from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('freelancer', 'Freelancer'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"
    
User = get_user_model()

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

#class Application(models.Model):
    #project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='applications')
    #freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    #applied_at = models.DateTimeField(auto_now_add=True)

    #def __str__(self):
        #return f"{self.freelancer.username} applied for {self.project.title}"
    
class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='applications')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.freelancer.username} - {self.project.title} ({self.status})"
