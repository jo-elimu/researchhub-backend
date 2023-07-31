from django.db import models

from .hub_v2 import HubV2


class DocumentHub(models.Model):
    document = models.ForeignKey(
        "researchhub_document.ResearchhubUnifiedDocument",
        on_delete=models.CASCADE,
        related_name="documenthub",
    )
    hub = models.ForeignKey(HubV2, on_delete=models.CASCADE, related_name="documenthub")

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return f"(Document {self.document.id} - Hub {self.hub.id}) association"
