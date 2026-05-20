from rest_framework import serializers
from .models import Application, Placement


class ApplicationSerializer(serializers.ModelSerializer):
    student_name      = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_reg       = serializers.CharField(source='student.registration_number', read_only=True)
    internship_title  = serializers.CharField(source='internship.title',            read_only=True)
    org_name          = serializers.CharField(source='internship.organization.company_name', read_only=True)

    class Meta:
        model  = Application
        fields = '__all__'
        read_only_fields = ['student', 'status', 'applied_at', 'reviewed_at']


class PlacementSerializer(serializers.ModelSerializer):
    student_name      = serializers.CharField(source='student.user.get_full_name',      read_only=True)
    organization_name = serializers.CharField(source='organization.company_name',       read_only=True)
    internship_title  = serializers.CharField(source='internship.title',                read_only=True)
    location          = serializers.CharField(source='internship.location',             read_only=True)

    class Meta:
        model  = Placement
        fields = '__all__'