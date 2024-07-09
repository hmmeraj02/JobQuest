from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile, Job, JobListing, JobApplication, JobCategory

class EmployerSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class JobSeekerSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    institution_name = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'institution_name', 'password1', 'password2']
        
class JobListingForm(forms.ModelForm):
    new_category = forms.CharField(max_length=100, required=False, help_text='Add a new category')

    class Meta:
        model = JobListing
        fields = ['title', 'description', 'requirements', 'location', 'company', 'category', 'new_category']

    def __init__(self, *args, **kwargs):
        super(JobListingForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = JobCategory.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        new_category = cleaned_data.get('new_category')

        if new_category:
            if JobCategory.objects.filter(name=new_category).exists():
                self.add_error('new_category', 'Category already exists.')
        
        return cleaned_data

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['resume', 'cover_letter']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['institution_name', 'gender', 'birth_date', 'hired']
