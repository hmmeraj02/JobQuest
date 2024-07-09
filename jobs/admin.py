from django.contrib import admin
from .models import User, JobListing, JobCategory, JobApplication

admin.site.register(User)
admin.site.register(JobListing)
admin.site.register(JobCategory)
admin.site.register(JobApplication)