from rest_framework.serializers import ModelSerializer, SerializerMethodField

from hub.related_models import DocumentHub

from .document_hub_action_serializer import DocumentHubActionSerializer


class DocumentHubSerializer(ModelSerializer):
    confidence_scores = DocumentHubActionSerializer(many=True)
    parent_resource_name = SerializerMethodField()
    resource_name = SerializerMethodField()

    class Meta:
        model = DocumentHub
        fields = ["parent_resource_name", "resource_name", "hub", "confidence_scores"]

    def get_parent_resource_name(self, obj: DocumentHub):
        return f"documents/{obj.document_id}"

    def get_resource_name(self, obj: DocumentHub):
        return f"documents/{obj.document_id}/hubs/{obj.hub_id}"

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
                if action["hub_provider"]["id"] == hub_provider_id
                and action["score"] >= float(min_confidence_score)
            ]
        elif hub_provider_id:
            # Filter out the actions that don't match the hub_provider_id filter
            data["confidence_scores"] = [
                action
                for action in data["confidence_scores"]
                if action["hub_provider"]["id"] == hub_provider_id
            ]
        elif min_confidence_score:
            # Filter out the actions that don't match the min_confidence_score filter
            data["confidence_scores"] = [
                action
                for action in data["confidence_scores"]
                if action["score"] >= float(min_confidence_score)
            ]

        return data
