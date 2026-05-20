import random
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import StudentProfile, OrganizationProfile, UniversityAdminProfile, SupervisorProfile, VerificationCode
from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer,
    StudentProfileSerializer, OrganizationProfileSerializer,
    UniversityAdminProfileSerializer, SupervisorProfileSerializer
)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Delete old unused codes
        VerificationCode.objects.filter(user=user, is_used=False).delete()

        # Generate 6-digit code
        code = str(random.randint(100000, 999999))
        expires_at = timezone.now() + timedelta(minutes=5)
        VerificationCode.objects.create(user=user, code=code, expires_at=expires_at)

        # Send code via email
        send_mail(
            subject='InternTrack - Your Verification Code',
            message=f'Your verification code is: {code}\n\nThis code expires in 5 minutes.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response({
            'message': 'Verification code sent to your email.',
            'email': user.email,
        }, status=status.HTTP_200_OK)


class VerifyCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        code  = request.data.get('code')

        try:
            from .models import CustomUser
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)

        verification = VerificationCode.objects.filter(
            user=user, code=code, is_used=False
        ).last()

        if not verification or not verification.is_valid():
            return Response({'detail': 'Invalid or expired code.'}, status=status.HTTP_400_BAD_REQUEST)

        # Mark code as used
        verification.is_used = True
        verification.save()

        # Return tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class SuperuserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if not user.is_superuser:
            return Response({'detail': 'Access denied. Superuser only.'}, status=status.HTTP_403_FORBIDDEN)
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class StudentProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, _ = StudentProfile.objects.get_or_create(user=self.request.user)
        return profile


class OrganizationProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = OrganizationProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, _ = OrganizationProfile.objects.get_or_create(user=self.request.user)
        return profile


class UniversityAdminProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UniversityAdminProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, _ = UniversityAdminProfile.objects.get_or_create(user=self.request.user)
        return profile


class SupervisorProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = SupervisorProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, _ = SupervisorProfile.objects.get_or_create(user=self.request.user)
        return profile
