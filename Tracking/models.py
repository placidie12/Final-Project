from django.db import models
from Applications.models import Placement


class ActivityLog(models.Model):
    LOG_TYPE_CHOICES = [
        ('daily',  'Daily Log'),
        ('weekly', 'Weekly Log'),
    ]
    STATUS_CHOICES = [
        ('pending',  'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    placement    = models.ForeignKey(Placement, on_delete=models.CASCADE, related_name='logs')
    log_type     = models.CharField(max_length=10, choices=LOG_TYPE_CHOICES, default='daily')
    date         = models.DateField()
    tasks_done   = models.TextField(help_text='What did the intern do today/this week?')
    skills_used  = models.TextField(blank=True, help_text='Which skills did they apply?')
    challenges   = models.TextField(blank=True, help_text='Any challenges faced?')
    hours_worked = models.DecimalField(max_digits=4, decimal_places=1, default=8.0)
    status       = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    supervisor_comment = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at  = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.placement.student.user.get_full_name()} - {self.date}'


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent',  'Absent'),
        ('late',    'Late'),
        ('excused', 'Excused'),
    ]

    placement = models.ForeignKey(Placement, on_delete=models.CASCADE, related_name='attendance')
    date      = models.DateField()
    status    = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    notes     = models.TextField(blank=True)
    marked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('placement', 'date')

    def __str__(self):
        return f'{self.placement.student.user.get_full_name()} - {self.date} - {self.status}'