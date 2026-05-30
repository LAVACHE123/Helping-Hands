from django.contrib import admin
from .models import Profile, Category, Job, Message, Review, JobApplication, Report


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'location')
    list_filter = ('role',)
    search_fields = ('user__username', 'location')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'requester', 'category', 'status', 'budget', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('title', 'description', 'location')
    list_editable = ('status',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('job', 'sender', 'created_at')
    search_fields = ('sender__username', 'job__title')


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('job__title', 'applicant__username')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'reviewee', 'job', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('reviewer__username', 'reviewee__username')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'reported_user', 'reported_job', 'created_at')
    search_fields = ('reporter__username',)
