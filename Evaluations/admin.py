from django.contrib import admin
from .models import Evaluation, Skill


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ['placement', 'overall_score', 'recommended', 'evaluated_at']
    list_filter  = ['recommended']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['skill_name', 'placement', 'level', 'added_at']
    list_filter  = ['level']
