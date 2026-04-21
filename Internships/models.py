from django.db import models
from accounts.models import OrganizationProfile

class InternshipPost(models.Model):
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('Canceled', 'Canceled'),
    ]

    TYPE_CHOICES = [
        ('Academic', 'Academic'),
        ('Professional', 'Professional'),
    ]

    OCCUPATION_CHOICES = [
        ('IT', 'Information Technology'),
        ('SD', 'Software Development'),
        ('DS', 'Data Science'),
        ('CS', 'Cybersecurity'),
        ('WD', 'Web Development'),
        ('AI', 'Artificial Intelligence'),
        ('ACC', 'Accounting'),
        ('FIN', 'Finance'),
        ('MKT', 'Marketing'),
        ('HR', 'Human Resources'),
        ('BA', 'Business Administration'),
        ('CE', 'Civil Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('EE', 'Electrical Engineering'),
        ('GD', 'Graphic Design'),
        ('MED', 'Medicine/Healthcare'),
        ('NUR', 'Nursing'),
        ('LAW', 'Law/Legal'),
        ('EDU', 'Education'),
        ('JRN', 'Journalism'),
        ('Other', 'Other'),
    ]

    organization = models.ForeignKey(OrganizationProfile, on_delete=models.CASCADE, related_name='internship_posts')
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField(help_text='List the requirements for the internship, separated by commas.')
    location = models.CharField(max_length=255)
    occupation = models.CharField(max_length=50, choices=OCCUPATION_CHOICES, help_text='Field or domain of the internship.')
    internship_type = models.CharField(max_length=20, choices=TYPE_CHOICES, help_text='Academic or Professional internship.')
    slots = models.PositiveIntegerField(default=1, help_text='Number of available positions.')
    duration = models.CharField(max_length=255, help_text='e.g., 3 months, 6 months.')
    start_date = models.DateField(help_text='The date when the internship starts.')
    end_date = models.DateField(help_text='The date when the internship ends.')
    deadline = models.DateField(help_text='The last date to apply for the internship.')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'({self.title}) at {self.organization.company_name}'

    def is_accepting_applications(self):
        from django.utils import timezone
        return self.status == 'Open' and self.deadline >= timezone.now().date()
    

   