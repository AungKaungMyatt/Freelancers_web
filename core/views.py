from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm
from .forms import ProjectForm
from .models import Project, Application
from django.shortcuts import get_object_or_404

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def client_dashboard(request):
    return render(request, 'client_dashboard.html')

@login_required
def freelancer_dashboard(request):
    return render(request, 'freelancer_dashboard.html')

class CustomLoginView(LoginView):
    def get_success_url(self):
        if self.request.user.role == 'client':
            return '/client/dashboard'
        elif self.request.user.role == 'freelancer':
            return '/freelancer/dashboard'
        return super().get_success_url()
    
@login_required
def post_project(request):
    if request.user.role != 'client':
        return redirect('login')  # Only clients can post projects
    
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            return redirect('client_dashboard')  # Redirect to client dashboard after posting
    else:
        form = ProjectForm()
    return render(request, 'post_project.html', {'form': form})

@login_required
def project_list(request):
    if request.user.role != 'freelancer':
        return redirect('login')  # Only freelancers can view this page

    projects = Project.objects.all()
    return render(request, 'project_list.html', {'projects': projects})

@login_required
def apply_project(request, project_id):
    if request.user.role != 'freelancer':
        return redirect('login')  # Only freelancers can apply

    project = get_object_or_404(Project, id=project_id)
    Application.objects.get_or_create(project=project, freelancer=request.user)
    return redirect('project_list')

@login_required
def view_applications(request, project_id):
    if request.user.role != 'client':
        return redirect('login')  # Only clients can access this page

    project = get_object_or_404(Project, id=project_id, created_by=request.user)
    applications = project.applications.all()  # Get all applications related to the project
    return render(request, 'view_applications.html', {'project': project, 'applications': applications})