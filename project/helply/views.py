from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm, JobForm, MessageForm, ProfileForm, ReviewForm, ReportForm
from django.contrib.auth.decorators import login_required
from .models import Job, Category, Message, Profile, Review, JobApplication, Report


def home_view(request):
    return render(request, 'home.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your account has been created.')
            if user.profile.role == 'requester':
                return redirect('job_create')
            else:
                return redirect('job_list')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    error = None
    username = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', 'home'))
        else:
            error = 'Invalid username or password.'
    return render(request, 'accounts/login.html', {
        'error': error,
        'username': username,
    })


def logout_view(request):
    logout(request)
    return redirect("login")


# ── Profile views ────────────────────────────────────────────────────────────

@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user, defaults={'role': 'helper'})
    jobs_posted = Job.objects.filter(requester=request.user)
    jobs_accepted = Job.objects.filter(helper=request.user)
    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'jobs_posted': jobs_posted,
        'jobs_accepted': jobs_accepted,
    })


@login_required
def profile_edit_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user, defaults={'role': 'helper'})
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile_edit.html', {'form': form})


def user_profile_view(request, user_id):
    viewed_user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=viewed_user)
    reviews = viewed_user.reviews_received.all()
    return render(request, 'accounts/user_profile.html', {
        'viewed_user': viewed_user,
        'profile': profile,
        'reviews': reviews,
    })


# ── Dashboard views ──────────────────────────────────────────────────────────

@login_required
def my_dashboard_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user, defaults={'role': 'helper'})
    if profile.role == 'requester':
        active_jobs = Job.objects.filter(requester=request.user, status__in=['open', 'accepted'])
        context = {'profile': profile, 'active_jobs': active_jobs}
    else:
        active_jobs = Job.objects.filter(helper=request.user, status='accepted')
        pending_applications = JobApplication.objects.filter(applicant=request.user, job__status='open')
        context = {
            'profile': profile,
            'active_jobs': active_jobs,
            'pending_applications': pending_applications,
        }
    return render(request, 'dashboard/my_jobs.html', context)


@login_required
def completed_jobs_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user, defaults={'role': 'helper'})
    if profile.role == 'requester':
        completed_jobs = Job.objects.filter(requester=request.user, status='completed')
    else:
        completed_jobs = Job.objects.filter(helper=request.user, status='completed')
    return render(request, 'dashboard/completed.html', {
        'profile': profile,
        'completed_jobs': completed_jobs,
    })


# ── Job views ────────────────────────────────────────────────────────────────

def job_list_view(request):
    jobs = Job.objects.filter(status='open')
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    if selected_category:
        jobs = jobs.filter(category__id=selected_category)
    return render(request, 'jobs/job_list.html', {
        'jobs': jobs,
        'categories': categories,
        'selected_category': selected_category,
    })


def job_detail_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    user_application = None
    if request.user.is_authenticated:
        user_application = JobApplication.objects.filter(job=job, applicant=request.user).first()
    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'user_application': user_application,
    })


@login_required
def job_create_view(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.requester = request.user
            job.save()
            messages.success(request, 'Your job has been posted!')
            return redirect('job_detail', job_id=job.id)
    else:
        form = JobForm()
    return render(request, 'jobs/job_create.html', {'form': form})


@login_required
def job_apply_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if job.status != 'open' or job.requester == request.user:
        messages.error(request, 'You cannot apply to this job.')
        return redirect('job_detail', job_id=job_id)
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.info(request, 'You have already applied to this job.')
        return redirect('job_detail', job_id=job_id)
    if request.method == 'POST':
        apply_message = request.POST.get('message', '')
        JobApplication.objects.create(job=job, applicant=request.user, message=apply_message)
        messages.success(request, 'Your application has been submitted!')
    return redirect('job_detail', job_id=job_id)


@login_required
def job_select_helper_view(request, job_id, user_id):
    job = get_object_or_404(Job, id=job_id)
    if job.requester != request.user or job.status != 'open':
        messages.error(request, 'You cannot perform this action.')
        return redirect('job_detail', job_id=job_id)
    selected_user = get_object_or_404(User, id=user_id)
    job.helper = selected_user
    job.status = 'accepted'
    job.save()
    messages.success(request, f'{selected_user.first_name} has been selected for this job!')
    return redirect('job_detail', job_id=job_id)


@login_required
def job_complete_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if job.requester == request.user and job.status == 'accepted':
        job.status = 'completed'
        job.save()
        messages.success(request, 'Job marked as completed!')
    return redirect('job_detail', job_id=job_id)


# ── Messaging ────────────────────────────────────────────────────────────────

@login_required
def message_thread_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.user != job.requester and request.user != job.helper:
        messages.error(request, 'You do not have access to this conversation.')
        return redirect('job_detail', job_id=job_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.job = job
            message.sender = request.user
            message.save()
            return redirect('message_thread', job_id=job_id)
    else:
        form = MessageForm()
    thread = Message.objects.filter(job=job).order_by('created_at')
    return render(request, 'messaging/thread.html', {
        'job': job,
        'thread': thread,
        'form': form,
    })


# ── Reports ──────────────────────────────────────────────────────────────────

@login_required
def report_create_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.user != job.requester and request.user != job.helper:
        raise PermissionDenied
    reported_user = job.helper if request.user == job.requester else job.requester
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.reported_user = reported_user
            report.reported_job = job
            report.save()
            messages.success(request, 'Your report has been submitted. We will review it shortly.')
            return redirect('completed_jobs')
    else:
        form = ReportForm()
    return render(request, 'reports/report_create.html', {
        'form': form,
        'job': job,
        'reported_user': reported_user,
    })


# ── Reviews ──────────────────────────────────────────────────────────────────

@login_required
def review_create_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if job.status != 'completed':
        messages.error(request, 'You can only review completed jobs.')
        return redirect('job_detail', job_id=job_id)
    if request.user != job.requester and request.user != job.helper:
        raise PermissionDenied
    reviewee = job.helper if request.user == job.requester else job.requester
    if Review.objects.filter(job=job, reviewer=request.user).exists():
        messages.error(request, 'You have already reviewed this job.')
        return redirect('job_detail', job_id=job_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.job = job
            review.reviewer = request.user
            review.reviewee = reviewee
            review.save()
            messages.success(request, 'Your review has been submitted!')
            return redirect('job_detail', job_id=job_id)
    else:
        form = ReviewForm()
    return render(request, 'reviews/review_create.html', {
        'form': form,
        'job': job,
        'reviewee': reviewee,
    })
