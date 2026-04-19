from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.utils import timezone
from .models import ActivityLog, Attendance
from .serializers import ActivityLogSerializer, AttendanceSerializer
from Applications.models import Placement
from accounts.models import StudentProfile, OrganizationProfile


class ActivityLogView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        role = request.user.role

        if role == 'student':
            try:
                student  = StudentProfile.objects.get(user=request.user)
                placement = Placement.objects.filter(student=student, status='active').first()
                if not placement:
                    return Response({'error': 'No active placement found'}, status=404)
                logs = ActivityLog.objects.filter(placement=placement)
            except StudentProfile.DoesNotExist:
                return Response({'error': 'Student profile not found'}, status=404)

        elif role == 'organization':
            try:
                org     = OrganizationProfile.objects.get(user=request.user)
                logs    = ActivityLog.objects.filter(placement__organization=org)
            except OrganizationProfile.DoesNotExist:
                return Response({'error': 'Organization profile not found'}, status=404)

        elif role == 'university_admin':
            logs = ActivityLog.objects.all()

        else:
            return Response({'error': 'Unauthorized'}, status=403)

        serializer = ActivityLogSerializer(logs, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            student   = StudentProfile.objects.get(user=request.user)
            placement = Placement.objects.filter(student=student, status='active').first()
            if not placement:
                return Response({'error': 'No active placement found'}, status=404)
        except StudentProfile.DoesNotExist:
            return Response({'error': 'Student profile not found'}, status=404)

        serializer = ActivityLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(placement=placement)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class LogApprovalView(APIView):
    """Supervisor approves or rejects a submitted log"""
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        try:
            log = ActivityLog.objects.get(pk=pk)
        except ActivityLog.DoesNotExist:
            return Response({'error': 'Log not found'}, status=404)

        if request.user.role != 'organization':
            return Response({'error': 'Only supervisors can approve logs'}, status=403)

        new_status = request.data.get('status')
        if new_status not in ['approved', 'rejected']:
            return Response({'error': 'Status must be approved or rejected'}, status=400)

        log.status             = new_status
        log.supervisor_comment = request.data.get('supervisor_comment', '')
        log.reviewed_at        = timezone.now()
        log.save()

        serializer = ActivityLogSerializer(log)
        return Response(serializer.data)


class AttendanceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        role = request.user.role
        if role == 'student':
            try:
                student   = StudentProfile.objects.get(user=request.user)
                placement = Placement.objects.filter(student=student, status='active').first()
                attendance = Attendance.objects.filter(placement=placement)
            except StudentProfile.DoesNotExist:
                return Response({'error': 'Student profile not found'}, status=404)
        elif role == 'organization':
            try:
                org        = OrganizationProfile.objects.get(user=request.user)
                attendance = Attendance.objects.filter(placement__organization=org)
            except OrganizationProfile.DoesNotExist:
                return Response({'error': 'Organization profile not found'}, status=404)
        else:
            attendance = Attendance.objects.all()

        serializer = AttendanceSerializer(attendance, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role != 'organization':
            return Response({'error': 'Only organizations can mark attendance'}, status=403)
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)