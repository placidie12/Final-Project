from django.contrib import admin
from .models import Application, Placement


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display  = ['student', 'internship', 'status', 'applied_at']
    list_filter   = ['status']
    search_fields = ['student__user__email', 'internship__title']


@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    list_display  = ['student', 'organization', 'internship', 'status', 'start_date', 'end_date']
    list_filter   = ['status']


