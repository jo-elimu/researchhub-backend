from rest_framework.serializers import ModelSerializer, SerializerMethodField

from hub.related_models import HubV2


class HubV2Serializer(ModelSerializer):
    resource_name = SerializerMethodField()

    class Meta:
        model = HubV2
        fields = ["id", "resource_name", "display_name", "description"]

    def get_resource_name(self, obj: HubV2):
        return f"hubs/{obj.id}"
