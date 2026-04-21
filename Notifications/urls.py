from django.urls import path
from . import views

urlpatterns = [
    path('',              views.NotificationView.as_view()),
    path('<int:pk>/',     views.MarkReadView.as_view()),
    path('read-all/',     views.MarkAllReadView.as_view()),
]