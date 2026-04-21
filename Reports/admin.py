from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display  = ('title', 'report_type', 'placement', 'generated_by', 'status', 'created_at')
    list_filter   = ('report_type', 'status')
    search_fields = ('title', 'placement__student__user__email')
