import rest_framework.serializers as serializers

from paper.models import PaperAuthor
from paper.serializers import DynamicPaperSerializer
from researchhub.serializers import DynamicModelFieldSerializer
from user.serializers import DynamicAuthorSerializer


class DynamicPaperAuthorSerializer(DynamicModelFieldSerializer):
    author = serializers.SerializerMethodField()
    # paper = serializers.SerializerMethodField()

    class Meta:
        model = PaperAuthor
        fields = "__all__"

    def get_author(self, paper_author):
        context = self.context
        _context_fields = context.get("pap_dpas_get_author", {})
        serializer = DynamicAuthorSerializer(
            paper_author.author, context=context, **_context_fields
        )
        return serializer.data

    def get_paper(self, paper_author):
        context = self.context
        _context_fields = context.get("pap_dpas_get_paper", {})
        serializer = DynamicPaperSerializer(
            paper_author.paper, context=context, **_context_fields
        )
        return serializer.data
