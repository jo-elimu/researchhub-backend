from rest_framework.serializers import ModelSerializer, SerializerMethodField

from hypothesis.models import Hypothesis
from paper.models import Paper
from researchhub_document.models import ResearchhubPost, ResearchhubUnifiedDocument
from researchhub_document.related_models.constants.document_type import (
    HYPOTHESIS,
    RESEARCHHUB_POST_DOCUMENT_TYPES,
)


class PostSerializer(ModelSerializer):
    class Meta(object):
        model = ResearchhubPost
        exclude = ["unified_document"]


class HypothesisSerializer(ModelSerializer):
    class Meta(object):
        model = Hypothesis
        exclude = ["unified_document"]


class PaperSerializer(ModelSerializer):
    class Meta(object):
        model = Paper
        exclude = ["hubs", "unified_document"]


class DocumentSerializer(ModelSerializer):
    details = SerializerMethodField()
    resource_name = SerializerMethodField()

    class Meta(object):
        model = ResearchhubUnifiedDocument
        fields = [
            "id",
            "resource_name",
            "document_type",
            "hot_score",
            "is_removed",
            "score",
            "details",
        ]

    def get_details(self, obj: ResearchhubUnifiedDocument):
        doc_type = obj.document_type
        if doc_type in RESEARCHHUB_POST_DOCUMENT_TYPES:
            return PostSerializer(obj.posts, many=True).data
        elif doc_type in [HYPOTHESIS]:
            return HypothesisSerializer(obj.hypothesis).data
        else:
            return PaperSerializer(obj.paper).data

    def get_resource_name(self, obj: ResearchhubUnifiedDocument):
        return f"documents/{obj.id}"
