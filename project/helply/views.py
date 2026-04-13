from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm, JobForm, MessageForm
from django.contrib.auth.decorators import login_required
from .models import Job, Category, Message 



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
            return redirect('home')
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
    job = Job.objects.get(id=job_id)
    return render(request, 'jobs/job_detail.html', {'job': job})


@login_required
def job_create_view(request):
    from .forms import JobForm
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.requester = request.user
            job.save()
            messages.success(request, 'Your job has been posted!')
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'jobs/job_create.html', {'form': form})


@login_required
def job_accept_view(request, job_id):
    job = Job.objects.get(id=job_id)
    if job.status == 'open' and job.requester != request.user:
        job.helper = request.user
        job.status = 'accepted'
        job.save()
        messages.success(request, 'You have accepted this job!')
    return redirect('job_detail', job_id=job_id)


@login_required
def job_complete_view(request, job_id):
    job = Job.objects.get(id=job_id)
    if job.requester == request.user and job.status == 'accepted':
        job.status = 'completed'
        job.save()
        messages.success(request, 'Job marked as completed!')
    return redirect('job_detail', job_id=job_id)

@login_required
def message_thread_view(request, job_id):
    job = Job.objects.get(id=job_id)

    # Only the requester or helper can see messages
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