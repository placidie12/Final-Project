from django.db import models
from accounts.models import StudentProfile, OrganizationProfile
from Internships.models import InternshipPost


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending',  'Pending'),
        ('reviewed', 'Reviewed'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    student      = models.ForeignKey(StudentProfile,  on_delete=models.CASCADE, related_name='applications')
    internship   = models.ForeignKey(InternshipPost,  on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True)
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at   = models.DateTimeField(auto_now_add=True)
    reviewed_at  = models.DateTimeField(null=True, blank=True)
    notes        = models.TextField(blank=True, help_text='Organization notes about this application')

    class Meta:
        unique_together = ('student', 'internship')

    def __str__(self):
        return f'{self.student.user.get_full_name()} → {self.internship.title}'


class Placement(models.Model):
    STATUS_CHOICES = [
        ('active',    'Active'),
        ('completed', 'Completed'),
        ('terminated','Terminated'),
    ]

    application  = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='placement')
    student      = models.ForeignKey(StudentProfile,     on_delete=models.CASCADE, related_name='placements')
    organization = models.ForeignKey(OrganizationProfile,on_delete=models.CASCADE, related_name='placements')
    internship   = models.ForeignKey(InternshipPost,     on_delete=models.CASCADE, related_name='placements')
    start_date   = models.DateField()
    end_date     = models.DateField()
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.user.get_full_name()} at {self.organization.company_name}'