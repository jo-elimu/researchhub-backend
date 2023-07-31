from django.db import models

from .hub_v2 import HubV2


class HubProvider(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    display_name = models.CharField(max_length=255)
    is_user = models.BooleanField()

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_removed = models.BooleanField(default=False)

    @property
    def hubs(self):
        return HubV2.objects.filter(metadata__hub_provider=self)

    def __str__(self):
        return self.display_name
