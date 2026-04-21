from django.db import models
from django.conf import settings
from Applications.models import Placement


class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ('internship', 'Internship Report'),
        ('placement',  'Placement Report'),
        ('evaluation', 'Evaluation Report'),
        ('attendance', 'Attendance Report'),
    ]
    STATUS_CHOICES = [
        ('draft',     'Draft'),
        ('published', 'Published'),
    ]

    title        = models.CharField(max_length=255)
    report_type  = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    placement    = models.ForeignKey(Placement, on_delete=models.CASCADE, related_name='reports')
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports')
    summary      = models.TextField(blank=True, help_text='Overall summary of the report.')
    status       = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.placement.student.user.get_full_name()}'
