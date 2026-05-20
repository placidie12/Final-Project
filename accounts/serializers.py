from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, StudentProfile, OrganizationProfile, UniversityAdminProfile, SupervisorProfile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'role', 'password']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        from .models import CustomUser
        try:
            user = CustomUser.objects.get(email=data['email'])
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials.")
        if not user.check_password(data['password']):
            raise serializers.ValidationError("Invalid credentials.")
        if not user.is_active:
            raise serializers.ValidationError("Account is disabled.")
        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'date_joined']


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = '__all__'
        read_only_fields = ['user']


class OrganizationProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationProfile
        fields = '__all__'
        read_only_fields = ['user']


class UniversityAdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversityAdminProfile
        fields = '__all__'
        read_only_fields = ['user']


class SupervisorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupervisorProfile
        fields = '__all__'
        read_only_fields = ['user']
