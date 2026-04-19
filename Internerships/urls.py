from django.urls import path
from .views import InternshipListView, InternshipDetailView, MyInternshipPostsView

urlpatterns = [
    path('', InternshipListView.as_view(), name='internship-list'),
    path('my-posts/', MyInternshipPostsView.as_view(), name='my-internship-posts'),
    path('<int:pk>/', InternshipDetailView.as_view(), name='internship-detail'),
]
