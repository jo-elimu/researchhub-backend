from django.db import connection, reset_queries
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from hub.related_models import DocumentHub, DocumentHubAction, HubV2
from hub.serializers import DocumentHubSerializer, HubV2Serializer
from hypothesis.models import Hypothesis
from paper.models import Paper
from researchhub_document.filters import DocumentFilter
from researchhub_document.models import ResearchhubPost, ResearchhubUnifiedDocument
from researchhub_document.related_models.constants.document_type import (
    HYPOTHESIS,
    RESEARCHHUB_POST_DOCUMENT_TYPES,
)
from researchhub_document.serializers import (
    HypothesisSerializer,
    PaperSerializer,
    PostSerializer,
)
from researchhub_document.views.custom.unified_document_pagination import (
    UnifiedDocPagination,
)
from utils.permissions import ReadOnly


class DocumentHubActionSerializer(ModelSerializer):
    class Meta:
        model = DocumentHubAction
        fields = ["hub_provider", "score", "created_date"]


class HubWithProviderActionsSerializer(ModelSerializer):
    confidence_scores = DocumentHubActionSerializer(many=True)

    class Meta:
        model = DocumentHub
        fields = ["hub", "confidence_scores"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        # Check if request has hub_provider_id and min_confidence_score query parameters
        hub_provider_id = request.query_params.get("hub_provider")
        min_confidence_score = request.query_params.get("min_confidence_score")

        if hub_provider_id and min_confidence_score:
            # Filter out the actions that don't match the filter
            data["confidence_scores"] = [
                action
                for action in data["confidence_scores"]
                if action["hub_provider"] == hub_provider_id
                and action["score"] >= float(min_confidence_score)
            ]
        elif hub_provider_id:
            # Filter out the actions that don't match the hub_provider_id filter
            data["confidence_scores"] = [
                action
                for action in data["confidence_scores"]
                if action["hub_provider"] == hub_provider_id
            ]
        elif min_confidence_score:
            # Filter out the actions that don't match the min_confidence_score filter
            data["confidence_scores"] = [
                action
                for action in data["confidence_scores"]
                if action["score"] >= float(min_confidence_score)
            ]

        return data


class DocumentWithHubsSerializer(ModelSerializer):
    details = SerializerMethodField()
    resource_name = SerializerMethodField()
    # documenthub = HubWithProviderActionsSerializer(many=True)
    hubs = SerializerMethodField()

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
            "hubs",
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

    def get_hubs(self, obj: ResearchhubUnifiedDocument):
        return [
            hub
            for hub in HubWithProviderActionsSerializer(
                obj.documenthub, many=True, context=self.context
            ).data
            if len(hub["confidence_scores"]) > 0
        ]


class DocumentViewSet(viewsets.ModelViewSet):
    """
    Used for:
      /api/documents/
      /api/documents/<document_id>
      /api/hubs/<hub_id>/documents/
      /api/hubs/<hub_id>/documents/<document_id>
    """

    permission_classes = [
        IsAuthenticated | ReadOnly,
    ]
    pagination_class = UnifiedDocPagination
    queryset = ResearchhubUnifiedDocument.objects.filter(is_removed=False)
    filter_backends = [DjangoFilterBackend]
    filter_class = DocumentFilter
    serializer_class = DocumentWithHubsSerializer

    def get_queryset(self):
        reset_queries()
        queryset = super().get_queryset()

        filters = []

        hub_id = self.kwargs.get("hub_id")
        if hub_id is not None:
            filters.append(Q(documenthub__hub_id=hub_id))

        min_confidence_score = self.request.query_params.get(
            "min_confidence_score", None
        )
        if min_confidence_score is not None:
            filters.append(
                Q(
                    documenthub__confidence_scores__score__gte=float(
                        min_confidence_score
                    )
                )
            )

        provider = self.request.query_params.get("hub_provider")
        if provider is not None:
            filters.append(Q(documenthub__confidence_scores__hub_provider=provider))

        queryset = queryset.prefetch_related("documenthub__confidence_scores").filter(
            *filters
        )

        return queryset.distinct()
