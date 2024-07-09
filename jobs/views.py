from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from .models import User, Profile, Job, JobListing, JobCategory, JobApplication
from .forms import EmployerSignUpForm, JobSeekerSignUpForm, JobListingForm, JobApplicationForm, UserUpdateForm, ProfileUpdateForm

def home(request):
    return render(request, 'jobs/home.html')

def logout_view(request):
    logout(request)
    return redirect('/')

# User Registration Views
class EmployerSignUpView(CreateView):
    model = User
    form_class = EmployerSignUpForm
    template_name = 'registration/employer_signup.html'
    success_url = reverse_lazy('employer_dashboard')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_employer = True
        user.save()
        login(self.request, user)
        return redirect(self.success_url)

class JobSeekerSignUpView(CreateView):
    model = User
    form_class = JobSeekerSignUpForm
    template_name = 'registration/job_seeker_signup.html'
    success_url = reverse_lazy('job_seeker_dashboard')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_job_seeker = True
        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        user.save()
        
        # Create and save the profile
        institution_name = form.cleaned_data.get('institution_name')
        Profile.objects.create(user=user, first_name=user.first_name, last_name=user.last_name, institution_name=institution_name)
        
        login(self.request, user)
        return redirect(self.success_url)

class JobCreateView(LoginRequiredMixin, CreateView):
    model = JobListing
    form_class = JobListingForm
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('job_listings')

    def form_valid(self, form):
        form.instance.employer = self.request.user  # Set the employer to the current user
        return super().form_valid(form)

class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = JobListing
    form_class = JobListingForm
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('job_listings')

    def test_func(self):
        job = self.get_object()
        # print(f"Job employer: {job.employer}, Current user: {self.request.user}")
        return self.request.user == job.employer
    
    def handle_no_permission(self):
        return HttpResponseForbidden("You do not have permission to edit this job.")

class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = JobListing
    template_name = 'jobs/job_confirm_delete.html'
    success_url = reverse_lazy('job_listings')

    def test_func(self):
        job = self.get_object()
        # print(f"Job employer: {job.employer}, Current user: {self.request.user}")
        return self.request.user == job.employer

    def handle_no_permission(self):
        return HttpResponseForbidden("You do not have permission to delete this job.")

# Job Listings
class JobListView(ListView):
    model = JobListing
    template_name = 'jobs/job_listings.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JobCategory.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        return context

class JobDetailView(DetailView):
    model = JobListing
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job'

class CreateJobListingView(LoginRequiredMixin, CreateView):
    model = JobListing
    form_class = JobListingForm
    template_name = 'jobs/create_job_listing.html'
    success_url = reverse_lazy('employer_dashboard')

    def form_valid(self, form):
        new_category_name = form.cleaned_data.get('new_category')
        if new_category_name:
            # Create the new category if it does not exist
            new_category, created = JobCategory.objects.get_or_create(name=new_category_name)
            form.instance.category = new_category

        job_listing = form.save(commit=False)
        job_listing.employer = self.request.user
        job_listing.save()
        return redirect(self.success_url)


class JobApplicationListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = JobApplication
    template_name = 'jobs/job_applications.html'
    context_object_name = 'applications'

    def get_queryset(self):
        self.job_listing = get_object_or_404(JobListing, id=self.kwargs['job_listing_id'])
        return JobApplication.objects.filter(job_listing=self.job_listing)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_listing'] = self.job_listing
        return context

    def test_func(self):
        job_listing = get_object_or_404(JobListing, id=self.kwargs['job_listing_id'])
        return self.request.user == job_listing.employer

class JobApplicationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = JobApplication
    template_name = 'jobs/job_application_confirm_delete.html'
    success_url = reverse_lazy('job_seeker_dashboard')

    def test_func(self):
        application = self.get_object()
        return self.request.user == application.job_seeker
    
# Dashboards
@login_required
def employer_dashboard(request):
    job_listings = request.user.job_listings.all()
    return render(request, 'jobs/employer_dashboard.html', {'job_listings': job_listings})

@login_required
def job_seeker_dashboard(request):
    applications = request.user.applications.all()
    return render(request, 'jobs/job_seeker_dashboard.html', {'applications': applications})

@login_required
def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)
            profile.first_name = user_form.cleaned_data['first_name']
            profile.last_name = user_form.cleaned_data['last_name']
            profile_form.save()
            return redirect('job_seeker_dashboard')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'jobs/profile_update.html', context)

# Job Applications
@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job_seeker = request.user
            application.job_listing = job
            application.save()
            send_mail(
                'Application Received',
                'Your application for the job has been received.',
                'from@example.com',
                [request.user.email],
                fail_silently=False,
            )
            return redirect('job_seeker_dashboard')
    else:
        form = JobApplicationForm()
    return render(request, 'jobs/apply_for_job.html', {'form': form, 'job': job})
