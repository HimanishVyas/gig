from rest_framework import serializers

from .models import Job


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = ["created_by", "created_at", "updated_at"]

    def create(self, validated_data):
        # Force created_by to be the authenticated user.
        user = self.context["request"].user
        return Job.objects.create(created_by=user, **validated_data)
