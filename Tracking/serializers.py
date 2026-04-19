from rest_framework import serializers
from .models import ActivityLog, Attendance


class ActivityLogSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='placement.student.user.get_full_name', read_only=True)
    org_name     = serializers.CharField(source='placement.organization.company_name',  read_only=True)

    class Meta:
        model  = ActivityLog
        fields = '__all__'
        read_only_fields = ['status', 'supervisor_comment', 'submitted_at', 'reviewed_at']


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='placement.student.user.get_full_name', read_only=True)

    class Meta:
        model  = Attendance
        fields = '__all__'