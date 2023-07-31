from django.db import models

from .document_hub import DocumentHub
from .hub_provider import HubProvider


class DocumentHubAction(models.Model):
    document_hub = models.ForeignKey(
        DocumentHub, on_delete=models.CASCADE, related_name="confidence_scores"
    )
    hub_provider = models.ForeignKey(HubProvider, on_delete=models.CASCADE)
    score = models.FloatField()

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return f"(Document {self.document.id} - Hub {self.hub.id}) association"
