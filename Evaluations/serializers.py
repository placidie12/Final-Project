from rest_framework import serializers
from .models import Evaluation, Skill


class EvaluationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='placement.student.user.get_full_name', read_only=True)
    org_name     = serializers.CharField(source='placement.organization.company_name',  read_only=True)

    class Meta:
        model  = Evaluation
        fields = '__all__'
        read_only_fields = ['overall_score', 'evaluated_at']

    def validate(self, data):
        for field in ['punctuality', 'technical_skills', 'communication', 'teamwork', 'initiative']:
            if field in data and not (1 <= data[field] <= 100):
                raise serializers.ValidationError(f'{field} must be between 1 and 100')
        return data


class SkillSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='placement.student.user.get_full_name', read_only=True)

    class Meta:
        model  = Skill
        fields = '__all__'