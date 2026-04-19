from django.urls import path
from . import views

urlpatterns = [
    path('logs/',              views.ActivityLogView.as_view()),
    path('logs/<int:pk>/approve/', views.LogApprovalView.as_view()),
    path('attendance/',        views.AttendanceView.as_view()),
]