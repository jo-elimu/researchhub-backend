from rest_framework import serializers

from user.serializers import MinimalUserSerializer


class GenericClaimCaseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    case_type = serializers.CharField()
    status = serializers.CharField()

    target_doi = serializers.SerializerMethodField()
    moderator = MinimalUserSerializer()
    requestor = MinimalUserSerializer()
    paper = serializers.SerializerMethodField()
    target_author_name = serializers.SerializerMethodField()
    provided_email = serializers.SerializerMethodField()

    def get_paper(self, case):
        if paper := getattr(case, "target_paper", None):
            obj = {
                "title": paper.title,
                "id": paper.id,
                "slug": paper.slug,
                "doi": paper.doi,
            }
            return obj
        return None

    def get_target_doi(self, case):
        if doi := getattr(case, "target_doi", None):
            return doi
        return None

    def get_target_author_name(self, case):
        if name := getattr(case, "target_author_name", None):
            return name
        return None

    def get_provided_email(self, case):
        if email := getattr(case, "provided_email", None):
            return email
        return None
