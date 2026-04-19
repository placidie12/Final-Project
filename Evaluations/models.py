from django.db import models
from Applications.models import Placement


class Evaluation(models.Model):
    placement        = models.ForeignKey(Placement, on_delete=models.CASCADE, related_name='evaluations')
    punctuality      = models.IntegerField(help_text='Score 1-100')
    technical_skills = models.IntegerField(help_text='Score 1-100')
    communication    = models.IntegerField(help_text='Score 1-100')
    teamwork         = models.IntegerField(help_text='Score 1-100')
    initiative       = models.IntegerField(help_text='Score 1-100')
    overall_score    = models.DecimalField(max_digits=5, decimal_places=1, editable=False, default=0)
    comments         = models.TextField(blank=True)
    recommended      = models.BooleanField(default=False, help_text='Would you recommend this student?')
    evaluated_at     = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        scores = [self.punctuality, self.technical_skills,
                  self.communication, self.teamwork, self.initiative]
        self.overall_score = round(sum(scores) / len(scores), 1)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Evaluation of {self.placement.student.user.get_full_name()} — {self.overall_score}/5'


class Skill(models.Model):
    LEVEL_CHOICES = [
        ('beginner',      'Beginner'),
        ('intermediate',  'Intermediate'),
        ('advanced',      'Advanced'),
    ]

    placement   = models.ForeignKey(Placement, on_delete=models.CASCADE, related_name='skills_gained')
    skill_name  = models.CharField(max_length=100)
    level       = models.CharField(max_length=15, choices=LEVEL_CHOICES, default='beginner')
    notes       = models.TextField(blank=True)
    added_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.skill_name} - {self.placement.student.user.get_full_name()}'