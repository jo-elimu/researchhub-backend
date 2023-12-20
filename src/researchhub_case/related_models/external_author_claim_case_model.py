from django.db import models

from researchhub_case.constants.case_constants import (
    APPROVED,
    AUTHOR_CLAIM_CASE_STATUS,
    DENIED,
    INITIATED,
)
from researchhub_case.related_models.researchhub_case_abstract_model import (
    AbstractResearchhubCase,
)
from researchhub_case.tasks import celery_add_author_citations


class ExternalAuthorClaimCase(AbstractResearchhubCase):
    h_index = models.IntegerField(default=0, null=True)
    publication_count = models.IntegerField(default=0, null=True)
    semantic_scholar_id = models.CharField(max_length=16, null=True)
    google_scholar_id = models.CharField(max_length=16, null=True)
    target_doi = models.CharField(max_length=255, null=True)
    status = models.CharField(
        choices=AUTHOR_CLAIM_CASE_STATUS,
        default=INITIATED,
        max_length=32,
        null=False,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["google_scholar_id", "requestor"],
                name="unique_google_scholar_id_claim",
            )
        ]

    def approve(self, should_save=True):
        requestor = self.requestor
        if not requestor.is_verified:
            requestor_author_profile = requestor.author_profile
            requestor.is_verified = True
            requestor_author_profile.is_verified = True
            requestor_author_profile.save(update_fields=["is_verified"])
            requestor.save(update_fields=["is_verified"])

        self.status = APPROVED
        if should_save:
            self.save(update_fields=["status"])

    def deny(self, should_save=True):
        self.status = DENIED
        if should_save:
            self.save(update_fields=["status"])

    def approve_google_scholar(self):
        celery_add_author_citations.apply_async(
            (self.requestor.id, self.google_scholar_id), priority=5, countdown=10
        )
        self.approve()
