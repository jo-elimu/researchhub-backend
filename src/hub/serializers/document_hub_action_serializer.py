from rest_framework.serializers import ModelSerializer

from hub.related_models import DocumentHubAction

from .hub_provider_serializer import HubProviderSerializer


class DocumentHubActionSerializer(ModelSerializer):
    hub_provider = HubProviderSerializer()

    class Meta:
        model = DocumentHubAction
        fields = ["hub_provider", "score", "created_date"]
