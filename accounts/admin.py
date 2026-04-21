from django.contrib import admin
from .models import CustomUser, StudentProfile, OrganizationProfile, UniversityAdminProfile


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display  = ['email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined']
    list_filter   = ['role', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display  = ['user', 'registration_number', 'university', 'department', 'year_of_study']
    search_fields = ['user__email', 'registration_number', 'university']


@admin.register(OrganizationProfile)
class OrganizationProfileAdmin(admin.ModelAdmin):
    list_display  = ['company_name', 'sector', 'location', 'contact_person']
    search_fields = ['company_name', 'sector']


@admin.register(UniversityAdminProfile)
class UniversityAdminProfileAdmin(admin.ModelAdmin):
    list_display  = ['user', 'university', 'department', 'position']
    search_fields = ['user__email', 'university']
