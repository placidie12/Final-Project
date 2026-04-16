from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("student", "Student"),
        ("organization", "Organization"),
        ("university_admin", "University Admin"),
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.email} ({self.role})"
    

class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="student_profile")
    registration_number = models.CharField(max_length=50, unique=True)
    university = models.CharField(max_length=150)
    department = models.CharField(max_length=150)
    year_of_study = models.IntegerField()
    phone_number = models.CharField(max_length=20)
    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    cv = models.FileField(upload_to="cvs/", blank=True, null=True)
    profile_photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.registration_number}"



class OrganizationProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="organization_profile")
    company_name = models.CharField(max_length=150)
    sector = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    website = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    contact_person = models.CharField(max_length=150)
    contact_phone = models.CharField(max_length=20)
    logo = models.ImageField(upload_to="org_logos/", blank=True, null=True)

    def __str__(self):
        return self.company_name


class UniversityAdminProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="university_admin_profile")
    university = models.CharField(max_length=150)
    department = models.CharField(max_length=150)
    position = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.university}"