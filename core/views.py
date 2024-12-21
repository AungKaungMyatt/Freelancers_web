from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm
from .forms import ProjectForm
from .models import Project, Application
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.views import View
from django.contrib.auth import update_session_auth_hash
from .forms import UserProfileForm, PasswordChangeForm

def home(request):
    return render(request, 'home.html')

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

class CustomLogoutView(View):
    def get(self, request):
        logout(request)  # Perform the logout
        return redirect('login')  # Redirect to login page

#@login_required
#def client_dashboard(request):
    #return render(request, 'client_dashboard.html')

@login_required
def client_dashboard(request):
    if request.user.role != 'client':
        return redirect('login')  # Only clients can access this page

    projects = Project.objects.filter(created_by=request.user)
    project_stats = []

    for project in projects:
        total_applications = project.applications.count()
        pending_applications = project.applications.filter(status='pending').count()
        project_stats.append({
            'project': project,
            'total_applications': total_applications,
            'pending_applications': pending_applications,
        })

    return render(request, 'client_dashboard.html', {'project_stats': project_stats})

@login_required
def freelancer_dashboard(request):
    if request.user.role != 'freelancer':
        return redirect('login')  # Only freelancers can access this page

    applications = request.user.applications.select_related('project')  # Get applied projects
    return render(request, 'freelancer_dashboard.html', {'applications': applications})


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

#@login_required
#def apply_project(request, project_id):
    #if request.user.role != 'freelancer':
        #return redirect('login')  # Only freelancers can apply

    #project = get_object_or_404(Project, id=project_id)
    #Application.objects.get_or_create(project=project, freelancer=request.user)
    #return redirect('project_list')

#@login_required
#def view_applications(request, project_id):
    #if request.user.role != 'client':
       # return redirect('login')  # Only clients can access this page

   # project = get_object_or_404(Project, id=project_id, created_by=request.user)
   # applications = project.applications.all()  # Get all applications related to the project
    #return render(request, 'view_applications.html', {'project': project, 'applications': applications})

@login_required
def apply_project(request, project_id):
    if request.user.role != 'freelancer':
        return redirect('login')  # Only freelancers can apply

    project = get_object_or_404(Project, id=project_id)

    # Check if the freelancer has already applied
    application, created = Application.objects.get_or_create(
        project=project,
        freelancer=request.user
    )
    if created:
        messages.success(request, f"You have successfully applied for '{project.title}'.")
    else:
        messages.warning(request, "You have already applied for this project.")

    return redirect('project_list')

@login_required
def view_applications(request, project_id):
    if request.user.role != 'client':
        return redirect('login')  # Only clients can access this page

    project = get_object_or_404(Project, id=project_id, created_by=request.user)

    # Handle POST request for accept/reject actions
    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        action = request.POST.get('action')

        application = get_object_or_404(Application, id=application_id, project=project)

        if action == 'accept':
            application.status = 'accepted'
            messages.success(request, f"Application from {application.freelancer.username} has been accepted.")
        elif action == 'reject':
            application.status = 'rejected'
            messages.warning(request, f"Application from {application.freelancer.username} has been rejected.")

        application.save()
        return redirect('view_applications', project_id=project.id)

    # Handle GET requests for filtering and sorting
    applications = project.applications.all()

    status_filter = request.GET.get('status')
    if status_filter in ['pending', 'accepted', 'rejected']:
        applications = applications.filter(status=status_filter)

    sort_by = request.GET.get('sort')
    if sort_by == 'date_asc':
        applications = applications.order_by('applied_at')
    elif sort_by == 'date_desc':
        applications = applications.order_by('-applied_at')

    return render(request, 'view_applications.html', {
        'project': project,
        'applications': applications,
        'status_filter': status_filter,
        'sort_by': sort_by
    })

@login_required
def profile(request):
    user = request.user

    # Handle user profile update
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user)
        password_form = PasswordChangeForm(request.POST)
        if 'update_profile' in request.POST and profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
        elif 'change_password' in request.POST and password_form.is_valid():
            if user.check_password(password_form.cleaned_data['old_password']):
                user.set_password(password_form.cleaned_data['new_password'])
                user.save()
                update_session_auth_hash(request, user)  # Keep user logged in after password change
                messages.success(request, "Password updated successfully!")
            else:
                messages.error(request, "Old password is incorrect!")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        profile_form = UserProfileForm(instance=user)
        password_form = PasswordChangeForm()

    return render(request, 'profile.html', {
        'profile_form': profile_form,
        'password_form': password_form
    })
