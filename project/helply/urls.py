
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # Jobs
    path('jobs/', views.job_list_view, name='job_list'),
    path('jobs/<int:job_id>/', views.job_detail_view, name='job_detail'),
    path('jobs/create/', views.job_create_view, name='job_create'),
    path('jobs/<int:job_id>/accept/', views.job_accept_view, name='job_accept'),
    path('jobs/<int:job_id>/complete/', views.job_complete_view, name='job_complete'),
    #messaging
    path('jobs/<int:job_id>/messages/', views.message_thread_view, name='message_thread'),
]