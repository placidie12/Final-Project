from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, LoginView, LogoutView,
    MeView, StudentProfileView, OrganizationProfileView,
    UniversityAdminProfileView, SuperuserLoginView
)

urlpatterns = [
    path('admin/login/', SuperuserLoginView.as_view(), name='superuser-login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MeView.as_view(), name='me'),
    path('me/student-profile/', StudentProfileView.as_view(), name='student-profile'),
    path('me/organization-profile/', OrganizationProfileView.as_view(), name='organization-profile'),
    path('me/university-admin-profile/', UniversityAdminProfileView.as_view(), name='university-admin-profile'),
]
