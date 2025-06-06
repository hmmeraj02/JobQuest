from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile, Job, JobListing, JobApplication, JobCategory
from .constants import GENDER_TYPE

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
    class Meta:
        model = JobListing
        fields = ['title', 'description', 'requirements', 'location', 'company', 'category']

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
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
    gender = forms.ChoiceField(choices=GENDER_TYPE, required=False)
