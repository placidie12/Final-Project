from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils import timezone
from .models import Application, Placement
from .serializers import ApplicationSerializer, PlacementSerializer
from accounts.models import StudentProfile, OrganizationProfile
from Internerships.models import InternshipPost


class StudentApplicationView(APIView):
  
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            student      = StudentProfile.objects.get(user=request.user)
            applications = Application.objects.filter(student=student).order_by('-applied_at')
            serializer   = ApplicationSerializer(applications, many=True)
            return Response(serializer.data)
        except StudentProfile.DoesNotExist:
            return Response({'error': 'Student profile not found'}, status=404)

    def post(self, request):
        try:
            student = StudentProfile.objects.get(user=request.user)
        except StudentProfile.DoesNotExist:
            return Response({'error': 'Complete your student profile first'}, status=400)

        internship_id = request.data.get('internship')
        try:
            internship = InternshipPost.objects.get(pk=internship_id)
        except InternshipPost.DoesNotExist:
            return Response({'error': 'Internship not found'}, status=404)

        if not internship.is_accepting_applications():
            return Response({'error': 'This internship is no longer accepting applications'}, status=400)

        if Application.objects.filter(student=student, internship=internship).exists():
            return Response({'error': 'You have already applied for this internship'}, status=400)

        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(student=student, internship=internship)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class OrgApplicationView(APIView):
    
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            org_profile  = OrganizationProfile.objects.get(user=request.user)
            applications = Application.objects.filter(
                internship__organization=org_profile
            ).order_by('-applied_at')
            serializer   = ApplicationSerializer(applications, many=True)
            return Response(serializer.data)
        except OrganizationProfile.DoesNotExist:
            return Response({'error': 'Organization profile not found'}, status=404)


class ApplicationDecisionView(APIView):
   
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        try:
            application = Application.objects.get(pk=pk)
        except Application.DoesNotExist:
            return Response({'error': 'Application not found'}, status=404)

        try:
            org_profile = OrganizationProfile.objects.get(user=request.user)
            if application.internship.organization != org_profile:
                return Response({'error': 'You can only manage your own applications'}, status=403)
        except OrganizationProfile.DoesNotExist:
            return Response({'error': 'Organization profile not found'}, status=404)

        new_status = request.data.get('status')
        if new_status not in ['approved', 'rejected', 'reviewed']:
            return Response({'error': 'Status must be approved, rejected, or reviewed'}, status=400)

        application.status      = new_status
        application.reviewed_at = timezone.now()
        application.notes       = request.data.get('notes', application.notes)
        application.save()

        if new_status == 'approved':
            Placement.objects.get_or_create(
                application  = application,
                defaults={
                    'student':      application.student,
                    'organization': org_profile,
                    'internship':   application.internship,
                    'start_date':   application.internship.start_date,
                    'end_date':     application.internship.end_date,
                }
            )

        serializer = ApplicationSerializer(application)
        return Response(serializer.data)


class PlacementListView(APIView):
   
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        role = request.user.role

        if role == 'student':
            try:
                student    = StudentProfile.objects.get(user=request.user)
                placements = Placement.objects.filter(student=student)
            except StudentProfile.DoesNotExist:
                return Response({'error': 'Student profile not found'}, status=404)

        elif role == 'organization':
            try:
                org_profile = OrganizationProfile.objects.get(user=request.user)
                placements  = Placement.objects.filter(organization=org_profile)
            except OrganizationProfile.DoesNotExist:
                return Response({'error': 'Organization profile not found'}, status=404)

        elif role == 'university_admin':
            placements = Placement.objects.all().order_by('-created_at')

        else:
            return Response({'error': 'Unauthorized'}, status=403)

        serializer = PlacementSerializer(placements, many=True)
        return Response(serializer.data)

