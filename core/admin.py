from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Project

# Register your models here.
# Registering CustomUser with UserAdmin @admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )

# Register the CustomUser model
admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'budget', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'created_by')