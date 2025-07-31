from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, JobForm, ApplicationForm
from .models import Job, Application
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data['role']
            group, created = Group.objects.get_or_create(name=role)
            user.groups.add(group)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form})

@login_required
def home_view(request):
    if request.user.groups.filter(name='employer').exists():
        return redirect('employer_dashboard')
    else:
        return redirect('applicant_dashboard')

#employer views

@login_required
def employer_dashboard(request):
    jobs = Job.objects.filter(posted_by=request.user)
    return render(request, 'myapp/employer_dashboard.html', {'jobs': jobs})

@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            return redirect('employer_dashboard')
    else:
        form = JobForm()
    return render(request, 'myapp/job_form.html', {'form': form})

@login_required
def applications_list(request, job_id):
    job = Job.objects.get(id=job_id)
    applications = Application.objects.filter(job=job)
    return render(request, 'myapp/applications_list.html', {'applications': applications, 'job': job})

#applicant views
@login_required
def applicant_dashboard(request):
    apps = Application.objects.filter(applicant=request.user)
    return render(request, 'myapp/applicant_dashboard.html', {'applications': apps})

def job_list(request):
    query = request.GET.get('q')
    jobs = Job.objects.all()
    if query:
        jobs = jobs.filter(title__icontains=query) | jobs.filter(company_name__icontains=query) | jobs.filter(location__icontains=query)
    return render(request, 'myapp/job_list.html', {'jobs': jobs})

def job_detail(request, job_id):
    job = Job.objects.get(id=job_id)
    return render(request, 'myapp/job_detail.html', {'job': job})

@login_required
def apply_job(request, job_id):
    job = Job.objects.get(id=job_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            return redirect('applicant_dashboard')
    else:
        form = ApplicationForm()
    return render(request, 'myapp/application_form.html', {'form': form, 'job': job})
