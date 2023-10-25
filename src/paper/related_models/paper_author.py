from django.db import models

from utils.models import DefaultModel


class PaperAuthor(DefaultModel):
    paper = models.ForeignKey("paper.Paper", on_delete=models.CASCADE)
    author = models.ForeignKey("user.Author", on_delete=models.CASCADE)
    ordinal = models.IntegerField(default=1)
