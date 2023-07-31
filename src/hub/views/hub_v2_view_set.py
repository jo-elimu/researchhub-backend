from rest_framework import pagination, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from hub.related_models import HubV2
from hub.serializers import HubV2Serializer


class HubV2Pagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 10000


class HubV2ViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Used for /api/hubs/
    """

    queryset = HubV2.objects.filter(is_removed=False)
    serializer_class = HubV2Serializer
    pagination_class = HubV2Pagination
    permission_classes = [IsAuthenticatedOrReadOnly]
