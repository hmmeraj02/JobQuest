from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('job_listings/', views.JobListView.as_view(), name='job_listings'),
    path('job/<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    path('job/new/', views.JobCreateView.as_view(), name='job_create'),
    path('job/<int:pk>/edit/', views.JobUpdateView.as_view(), name='job_update'),
    path('job/<int:pk>/delete/', views.JobDeleteView.as_view(), name='job_delete'),
    path('employer/signup/', views.EmployerSignUpView.as_view(), name='employer_signup'),
    path('job_seeker/signup/', views.JobSeekerSignUpView.as_view(), name='job_seeker_signup'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('job_seeker/dashboard/', views.job_seeker_dashboard, name='job_seeker_dashboard'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('application/<int:pk>/delete/', views.JobApplicationDeleteView.as_view(), name='job_application_delete'),
    path('apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('job/<int:job_listing_id>/applications/', views.JobApplicationListView.as_view(), name='job_applications'),
    path('accounts/logout/', views.logout_view, name='logout'),
]
