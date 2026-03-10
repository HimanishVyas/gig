from rest_framework import serializers

from auth.models import User
from .models import Bid, Job, JobStatus


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = ["created_by", "created_at", "updated_at"]

    def create(self, validated_data):
        # Force created_by to be the authenticated user.
        user = self.context["request"].user
        return Job.objects.create(created_by=user, **validated_data)


class WorkerBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "display_name", "first_name", "last_name", "email"]
        read_only_fields = fields


class BidSerializer(serializers.ModelSerializer):
    worker = WorkerBasicSerializer(read_only=True)

    class Meta:
        model = Bid
        fields = "__all__"
        read_only_fields = ["id", "job", "worker", "status", "created_at"]

    def validate(self, attrs):
        request = self.context["request"]
        job = self.context["job"]
        worker = request.user

        if job.created_by_id == worker.id:
            raise serializers.ValidationError("You cannot bid on your own job.")

        if Bid.objects.filter(job=job, worker=worker).exists():
            raise serializers.ValidationError("You have already placed a bid on this job.")

        if job.status != JobStatus.OPEN:
            raise serializers.ValidationError("Bids can be placed only on OPEN jobs.")

        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        job = self.context["job"]
        worker = request.user
        return Bid.objects.create(job=job, worker=worker, **validated_data)


class BidListSerializer(serializers.ModelSerializer):
    worker = WorkerBasicSerializer(read_only=True)

    class Meta:
        model = Bid
        fields = "__all__"
        read_only_fields = fields


class WorkerBidSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)

    class Meta:
        model = Bid
        fields = "__all__"
        read_only_fields = fields
