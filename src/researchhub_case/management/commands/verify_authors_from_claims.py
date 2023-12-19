from django.core.management.base import BaseCommand

from researchhub_case.constants.case_constants import APPROVED
from researchhub_case.models import AuthorClaimCase


class Command(BaseCommand):
    def handle(self, *args, **options):
        claims = AuthorClaimCase.objects.filter(
            status=APPROVED, requestor__isnull=False
        ).distinct("requestor")
        claims_count = claims.count()

        for i, claim in enumerate(claims.iterator()):
            print(f"{i}/{claims_count}")
            requestor = claim.requestor
            requestor_author_profile = requestor.author_profile
            if not requestor.is_verified:
                requestor.is_verified = True
                requestor_author_profile.is_verified = True
                requestor_author_profile.save(update_fields=["is_verified"])
                requestor.save(update_fields=["is_verified"])
        print("Finished")
