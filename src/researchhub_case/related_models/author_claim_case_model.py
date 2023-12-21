from django.db import models

from paper.models import Paper
from reputation.models import Escrow
from researchhub_case.constants.case_constants import (
    AUTHOR_CLAIM_CASE_STATUS,
    INITIATED,
)
from researchhub_case.related_models.researchhub_case_abstract_model import (
    AbstractResearchhubCase,
)
from user.models import Author


class AuthorClaimCase(AbstractResearchhubCase):
    provided_email = models.EmailField(
        blank=False,
        help_text=(
            "Requestors may use this field to validate themselves with this email"
        ),
        null=False,
    )
    status = models.CharField(
        choices=AUTHOR_CLAIM_CASE_STATUS,
        default=INITIATED,
        max_length=32,
        null=False,
    )
    # TODO: Deprecate in next iteration. No longer used.
    target_author = models.ForeignKey(
        Author,
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name="related_claim_cases",
    )
    target_paper = models.ForeignKey(
        Paper,
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name="related_claim_cases",
    )
    target_author_name = models.CharField(
        max_length=255,
        null=True,
        blank=False,
    )
    claimed_rsc = models.ManyToManyField(Escrow, blank=True, related_name="claim_case")
