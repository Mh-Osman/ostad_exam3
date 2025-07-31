from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Employer
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('employer/post-job/', views.post_job, name='post_job'),
    path('employer/job/<int:job_id>/applications/', views.applications_list, name='applications_list'),

    # Applicant
    path('applicant/dashboard/', views.applicant_dashboard, name='applicant_dashboard'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/<int:job_id>/apply/', views.apply_job, name='apply_job'),
]
