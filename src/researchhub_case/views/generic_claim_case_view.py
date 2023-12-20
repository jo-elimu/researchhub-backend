from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from hub.permissions import IsModerator
from researchhub_case.models import AuthorClaimCase, ExternalAuthorClaimCase
from researchhub_case.serializers import GenericClaimCaseSerializer


class ClaimCaseView(GenericViewSet):
    ordering = ["-updated_date"]
    pagination_size = 10
    permission_classes = [IsAuthenticated, IsModerator]
    serializer_class = GenericClaimCaseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]

    def get_queryset(self):
        return AuthorClaimCase.objects.all(), ExternalAuthorClaimCase.objects.all()

    def list(self, request):
        internal_claim_qs, external_claim_qs = self.get_queryset()
        internal_claim_qs = self.filter_queryset(internal_claim_qs)
        external_claim_qs = self.filter_queryset(external_claim_qs)

        internal_page = self.paginate_queryset(internal_claim_qs)
        external_page = self.paginate_queryset(external_claim_qs)

        internal_serializer = self.get_serializer(internal_page, many=True)
        external_serializer = self.get_serializer(external_page, many=True)
        internal_response = self.get_paginated_response(internal_serializer.data)
        external_response = self.get_paginated_response(external_serializer.data)
        internal_response.data.update(external_response.data)
        return internal_response
