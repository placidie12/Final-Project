from django.contrib import admin
from .models import InternshipPost


@admin.register(InternshipPost)
class InternshipPostAdmin(admin.ModelAdmin):
    list_display   = ['title', 'organization', 'status', 'deadline', 'slots', 'created_at']
    list_filter    = ['status', 'occupation', 'internship_type']
    search_fields  = ['title', 'description', 'organization__company_name']
    ordering       = ['-created_at']