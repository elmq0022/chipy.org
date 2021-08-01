from django.db.models import fields
from rest_framework import serializers

from chipy_org.apps.job_board.models import (
    JobPost,
    STATUS_CHOICES,
    LOCATION_CHOICES,
    JOB_TYPE_CHOICES,
    MAX_LENGTH,
    NUM_DAYS_T0_EXPIRE,
)


class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = [
            "company_name",
            "position",
            "description",
            "is_sponsor",
            "can_host_meeting",
            "location",
            "job_type",
            "company_website",
            "how_to_apply",
            "agree_to_terms",
            "is_from_recruiting_agency",
        ]
