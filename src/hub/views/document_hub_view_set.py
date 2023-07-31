from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from hub.related_models import DocumentHub
from hub.serializers import DocumentHubSerializer


class DocumentHubViewSet(viewsets.ModelViewSet):
    """
    Used for /api/documents/<doc_id>/hubs/
    """

    queryset = DocumentHub.objects.all()
    serializer_class = DocumentHubSerializer
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        document_id = self.kwargs.get("document_id")
        if document_id is not None:
            return DocumentHub.objects.filter(document_id=document_id)

        hub_id = self.kwargs.get("hub_id")
        return DocumentHub.objects.filter(hub_id=hub_id)

    def get_object(self):
        document_id = self.kwargs.get("document_id") or self.kwargs["pk"]
        hub_id = self.kwargs.get("hub_id") or self.kwargs["pk"]
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(hub_id=hub_id, document_id=document_id)
        self.check_object_permissions(self.request, obj)
        return obj

    @action(detail=True, methods=["GET"])
    def document_hub_association(self, request, document_id=None, hub_id=None):
        document_hub = self.get_object()
        serializer = self.get_serializer(document_hub)
        return Response(serializer.data)

    def filter_queryset(self, queryset):
        # Get the query parameters from the request
        hub_provider_id = self.request.query_params.get("hub_provider")
        min_confidence_score = self.request.query_params.get("min_confidence_score")

        # If both hub_provider and min_confidence_score are provided, apply
        # both filters
        if hub_provider_id and min_confidence_score:
            queryset = queryset.filter(
                confidence_scores__hub_provider_id=hub_provider_id,
                confidence_scores__score__gte=float(min_confidence_score),
            )
        # If only hub_provider is provided, apply that filter
        elif hub_provider_id:
            queryset = queryset.filter(
                confidence_scores__hub_provider_id=hub_provider_id
            )
        # If only min_confidence_score is provided, apply that filter
        elif min_confidence_score:
            queryset = queryset.filter(
                confidence_scores__score__gte=float(min_confidence_score)
            )

        return queryset
