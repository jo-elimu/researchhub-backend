from rest_framework.serializers import ModelSerializer

from researchhub_case.models import ExternalAuthorClaimCase
from researchhub_case.tasks import trigger_email_validation_flow

from .abstract_researchhub_case_serializer import DynamicAbstractResearchhubCase
from .researchhub_case_abstract_serializer import EXPOSABLE_FIELDS


class ExternalAuthorClaimCaseSerializer(ModelSerializer):
    class Meta:
        model = ExternalAuthorClaimCase
        fields = [
            *EXPOSABLE_FIELDS,
            "google_scholar_id",
            "h_index",
            "publication_count",
            "provided_email",
            "status",
            "semantic_scholar_id",
            "target_doi",
        ]
        read_only_fields = [
            "created_date",
            "id",
            "moderator",
            "status",
            "updated_date,",
        ]

    def create(self, validated_data):
        res = super().create(validated_data)
        trigger_email_validation_flow.apply_async(
            (res.id, "EXTERNAL"), priority=2, countdown=5
        )
        return res


class DynamicExternalAuthorClaimCaseSerializer(DynamicAbstractResearchhubCase):
    class Meta:
        model = ExternalAuthorClaimCase
        fields = "__all__"
