from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomLoginView
from .views import CustomLogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('client/dashboard', views.client_dashboard, name='client_dashboard'),
    path('freelancer/dashboard', views.freelancer_dashboard, name='freelancer_dashboard'),
    path('post_project/', views.post_project, name='post_project'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:project_id>/apply/', views.apply_project, name='apply_project'),
    path('projects/<int:project_id>/applications/', views.view_applications, name='view_applications'),
    path('profile/', views.profile, name='profile'),
]