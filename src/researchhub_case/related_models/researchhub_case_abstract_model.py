from django.db import models

from researchhub_case.constants.case_constants import RH_CASE_TYPES
from utils.models import DefaultModel


class AbstractResearchhubCase(DefaultModel):
    case_type = models.CharField(
        blank=False,
        choices=RH_CASE_TYPES,
        max_length=32,
        null=False,
    )
    creator = models.ForeignKey(
        "user.User",
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name="%(class)s_created_cases",
    )
    moderator = models.ForeignKey(
        "user.User",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="%(class)s_moderating_cases",
    )
    requestor = models.ForeignKey(
        "user.User",
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name="%(class)s_requested_cases",
    )
    provided_email = models.EmailField(
        blank=False,
        help_text=(
            "Requestors may use this field to validate themselves with this email"
        ),
        null=False,
    )
    token_generated_time = models.IntegerField(
        blank=True,
        default=None,
        help_text="Intentionally setting as a int field",
        null=True,
    )
    validation_attempt_count = models.IntegerField(
        blank=False,
        default=-1,
        help_text="Number of attempts to validate themselves given token",
        null=False,
    )
    validation_token = models.CharField(
        blank=True,
        db_index=True,
        default=None,
        max_length=255,
        null=True,
        unique=True,
    )

    class Meta:
        abstract = True
