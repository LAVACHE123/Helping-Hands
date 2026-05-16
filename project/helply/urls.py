from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # Profile
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('users/<int:user_id>/', views.user_profile_view, name='user_profile'),
    # Dashboard
    path('dashboard/', views.my_dashboard_view, name='dashboard'),
    path('dashboard/completed/', views.completed_jobs_view, name='completed_jobs'),
    # Jobs
    path('jobs/', views.job_list_view, name='job_list'),
    path('jobs/create/', views.job_create_view, name='job_create'),
    path('jobs/<int:job_id>/', views.job_detail_view, name='job_detail'),
    path('jobs/<int:job_id>/apply/', views.job_apply_view, name='job_apply'),
    path('jobs/<int:job_id>/select/<int:user_id>/', views.job_select_helper_view, name='job_select_helper'),
    path('jobs/<int:job_id>/complete/', views.job_complete_view, name='job_complete'),
    # Messaging
    path('jobs/<int:job_id>/messages/', views.message_thread_view, name='message_thread'),
    # Reviews
    path('jobs/<int:job_id>/review/', views.review_create_view, name='review_create'),
    # Reports
    path('jobs/<int:job_id>/report/', views.report_create_view, name='report_create'),
]
