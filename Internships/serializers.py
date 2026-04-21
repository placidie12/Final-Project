from rest_framework import serializers
from .models import InternshipPost


class InternshipPostSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.company_name', read_only=True)
    organization_location = serializers.CharField(source='organization.location', read_only=True)
    is_accepting = serializers.SerializerMethodField()

    class Meta:
        model = InternshipPost
        fields = '__all__'
        read_only_fields = ['organization', 'status', 'created_at', 'updated_at']

    def get_is_accepting(self, obj):
        return obj.is_accepting_applications()

    def validate_deadline(self, value):
        from django.utils import timezone
        if value < timezone.now().date():
            raise serializers.ValidationError("Deadline must be a future date.")
        return value

    def validate_slots(self, value):
        if value < 1:
            raise serializers.ValidationError('Slots must be at least 1.')
        return value
