from django.urls import path
from . import views

urlpatterns = [
    path('',                     views.StudentApplicationView.as_view()),
    path('org/',                 views.OrgApplicationView.as_view()),
    path('<int:pk>/decision/',   views.ApplicationDecisionView.as_view()),
    path('placements/',          views.PlacementListView.as_view()),
]