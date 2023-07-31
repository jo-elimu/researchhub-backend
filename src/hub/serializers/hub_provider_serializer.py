from rest_framework.serializers import ModelSerializer, SerializerMethodField

from hub.related_models import HubProvider


class HubProviderSerializer(ModelSerializer):
    resource_name = SerializerMethodField()

    class Meta:
        model = HubProvider
        fields = ["id", "resource_name", "display_name", "is_user"]

    def get_resource_name(self, obj: HubProvider):
        return f"hub-providers/{obj.id}"
