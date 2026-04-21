from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from Applications.models import Application, Placement
from Tracking.models import ActivityLog
from Evaluations.models import Evaluation
from accounts.models import StudentProfile, OrganizationProfile
from django.db.models import Avg, Count


class IsUniversityAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'university_admin'


class AdminReportView(APIView):
    permission_classes = [IsUniversityAdmin]

    def get(self, request):
        total_students     = StudentProfile.objects.count()
        total_orgs         = OrganizationProfile.objects.count()
        total_applications = Application.objects.count()
        total_placements   = Placement.objects.count()
        active_placements  = Placement.objects.filter(status='active').count()
        completed          = Placement.objects.filter(status='completed').count()
        avg_score          = Evaluation.objects.aggregate(avg=Avg('overall_score'))['avg']
        pending_logs       = ActivityLog.objects.filter(status='pending').count()

        return Response({
            'total_students':     total_students,
            'total_organizations':total_orgs,
            'total_applications': total_applications,
            'total_placements':   total_placements,
            'active_placements':  active_placements,
            'completed_internships': completed,
            'average_evaluation_score': round(avg_score, 2) if avg_score else 0,
            'pending_logs_to_review':  pending_logs,
        })