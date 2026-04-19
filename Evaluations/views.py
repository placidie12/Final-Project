from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import Evaluation, Skill
from .serializers import EvaluationSerializer, SkillSerializer
from Applications.models import Placement
from accounts.models import StudentProfile, OrganizationProfile


class EvaluationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        role = request.user.role
        if role == 'student':
            try:
                student      = StudentProfile.objects.get(user=request.user)
                placements   = Placement.objects.filter(student=student)
                evaluations  = Evaluation.objects.filter(placement__in=placements)
            except StudentProfile.DoesNotExist:
                return Response({'error': 'Student profile not found'}, status=404)

        elif role == 'organization':
            try:
                org         = OrganizationProfile.objects.get(user=request.user)
                evaluations = Evaluation.objects.filter(placement__organization=org)
            except OrganizationProfile.DoesNotExist:
                return Response({'error': 'Organization profile not found'}, status=404)

        else:
            evaluations = Evaluation.objects.all()

        serializer = EvaluationSerializer(evaluations, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role != 'organization':
            return Response({'error': 'Only organizations can submit evaluations'}, status=403)

        serializer = EvaluationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class EvaluationDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Evaluation.objects.get(pk=pk)
        except Evaluation.DoesNotExist:
            return None

    def put(self, request, pk):
        if request.user.role != 'organization':
            return Response({'error': 'Only organizations can update evaluations'}, status=403)
        evaluation = self.get_object(pk)
        if not evaluation:
            return Response({'error': 'Evaluation not found'}, status=404)
        serializer = EvaluationSerializer(evaluation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        if request.user.role != 'organization':
            return Response({'error': 'Only organizations can delete evaluations'}, status=403)
        evaluation = self.get_object(pk)
        if not evaluation:
            return Response({'error': 'Evaluation not found'}, status=404)
        evaluation.delete()
        return Response(status=204)


class SkillView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role == 'student':
            try:
                student    = StudentProfile.objects.get(user=request.user)
                placements = Placement.objects.filter(student=student)
                skills     = Skill.objects.filter(placement__in=placements)
            except StudentProfile.DoesNotExist:
                return Response({'error': 'Student profile not found'}, status=404)
        else:
            skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class SkillDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Skill.objects.get(pk=pk)
        except Skill.DoesNotExist:
            return None

    def put(self, request, pk):
        skill = self.get_object(pk)
        if not skill:
            return Response({'error': 'Skill not found'}, status=404)
        serializer = SkillSerializer(skill, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        skill = self.get_object(pk)
        if not skill:
            return Response({'error': 'Skill not found'}, status=404)
        skill.delete()
        return Response(status=204)