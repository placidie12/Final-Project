from django.contrib import admin
from .models import ActivityLog, Attendance


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display  = ['placement', 'date', 'log_type', 'hours_worked', 'status']
    list_filter   = ['status', 'log_type']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display  = ['placement', 'date', 'status']
    list_filter   = ['status']