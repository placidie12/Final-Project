"""
URL configuration for internship_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.shortcuts import render
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

def home(request):
    return render(request, 'landing/index.html')

def login_page(request):
    return render(request, 'Authentication/login.html')

def register_page(request):
    return render(request, 'Authentication/register.html')

def internships_page(request):
    return render(request, 'student/internships.html')

def about_page(request):
    return render(request, 'Landing/about.html')

def contact_page(request):
    return render(request, 'Landing/contact.html')

def student_dashboard(request):
    return render(request, 'student/dashboard.html')

def student_profile(request):
    return render(request, 'student/profile.html')

def student_internships(request):
    return render(request, 'student/internships.html')

def student_applications(request):
    return render(request, 'student/applications.html')

def student_logs(request):
    return render(request, 'student/logs.html')

def student_evaluations(request):
    return render(request, 'student/evaluations.html')

def organization_dashboard(request):
    return render(request, 'Organization/dashboard.html')

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('about/', about_page, name='about'),
    path('contact/', contact_page, name='contact'),
    path('internships/', internships_page, name='internships'),
    path('dashboard/student/', student_dashboard, name='student-dashboard'),
    path('dashboard/organization/', organization_dashboard, name='organization-dashboard'),
    path('profile/student/', student_profile, name='student-profile'),
    path('internships/', student_internships, name='student-internships'),
    path('applications/', student_applications, name='student-applications'),
    path('tracking/', student_logs, name='student-logs'),
    path('evaluations/', student_evaluations, name='student-evaluations'),
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/internships/', include('Internships.urls')),
    path('api/applications/', include('Applications.urls')),
    path('api/tracking/', include('Tracking.urls')),
    path('api/evaluations/', include('Evaluations.urls')),
    path('api/notifications/', include('Notifications.urls')),
    path('api/reports/', include('Reports.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
