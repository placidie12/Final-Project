from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import InternshipPost
from .serializers import InternshipPostSerializer
from accounts.models import OrganizationProfile


class IsOrganization(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'organization'


class IsUniversityAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'university_admin'


class InternshipListView(APIView):
    """
    GET  - anyone logged in can browse all open internships
    POST - only organizations can create a new internship post
    """
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsOrganization()]
        return [permissions.IsAuthenticated()]

    def get(self, request):
        internships = InternshipPost.objects.filter(status='Open').order_by('-created_at')

        occupation = request.query_params.get('occupation')
        if occupation:
            internships = internships.filter(occupation__icontains=occupation)

        internship_type = request.query_params.get('internship_type')
        if internship_type:
            internships = internships.filter(internship_type__icontains=internship_type)

        location = request.query_params.get('location')
        if location:
            internships = internships.filter(location__icontains=location)

       
        search = request.query_params.get('search')
        if search:
            from django.db.models import Q
            internships = internships.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        serializer = InternshipPostSerializer(internships, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            org_profile = OrganizationProfile.objects.get(user=request.user)
        except OrganizationProfile.DoesNotExist:
            return Response(
                {'error': 'Please complete your organization profile first'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = InternshipPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(organization=org_profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InternshipDetailView(APIView):
    """
    GET    - view a single internship detail
    PUT    - organization edits their own internship
    DELETE - organization deletes their own internship
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return InternshipPost.objects.get(pk=pk)
        except InternshipPost.DoesNotExist:
            return None

    def get(self, request, pk):
        internship = self.get_object(pk)
        if not internship:
            return Response({'error': 'Internship not found'}, status=404)
        serializer = InternshipPostSerializer(internship)
        return Response(serializer.data)

    def put(self, request, pk):
        internship = self.get_object(pk)
        if not internship:
            return Response({'error': 'Internship not found'}, status=404)

      
        if request.user.role != 'organization':
            return Response({'error': 'Only organizations can edit internships'}, status=403)

        try:
            org_profile = OrganizationProfile.objects.get(user=request.user)
            if internship.organization != org_profile:
                return Response({'error': 'You can only edit your own internships'}, status=403)
        except OrganizationProfile.DoesNotExist:
            return Response({'error': 'Organization profile not found'}, status=404)

        serializer = InternshipPostSerializer(internship, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        internship = self.get_object(pk)
        if not internship:
            return Response({'error': 'Internship not found'}, status=404)

        if request.user.role != 'organization':
            return Response({'error': 'Only organizations can delete internships'}, status=403)

        try:
            org_profile = OrganizationProfile.objects.get(user=request.user)
            if internship.organization != org_profile:
                return Response({'error': 'You can only delete your own internships'}, status=403)
        except OrganizationProfile.DoesNotExist:
            return Response({'error': 'Organization profile not found'}, status=404)

        internship.delete()
        return Response({'message': 'Internship deleted successfully'}, status=204)


class MyInternshipPostsView(APIView):
    """
    GET - organization sees only their own posted internships
    """
    permission_classes = [IsOrganization]

    def get(self, request):
        try:
            org_profile = OrganizationProfile.objects.get(user=request.user)
            internships = InternshipPost.objects.filter(
                organization=org_profile
            ).order_by('-created_at')
            serializer  = InternshipPostSerializer(internships, many=True)
            return Response(serializer.data)
        except OrganizationProfile.DoesNotExist:
            return Response({'error': 'Organization profile not found'}, status=404)