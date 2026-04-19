from django.urls import path
from . import views

urlpatterns = [
    path('',                views.EvaluationView.as_view()),
    path('<int:pk>/',       views.EvaluationDetailView.as_view()),
    path('skills/',         views.SkillView.as_view()),
    path('skills/<int:pk>/', views.SkillDetailView.as_view()),
]