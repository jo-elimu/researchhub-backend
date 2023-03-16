# Generated by Django 4.1 on 2023-03-16 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("researchhub_comment", "0010_alter_rhcommentmodel_comment_content_src"),
    ]

    operations = [
        migrations.AddField(
            model_name="rhcommentmodel",
            name="is_public",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="rhcommentmodel",
            name="is_removed",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="rhcommentmodel",
            name="legacy_model_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("LEGACY_COMMENT", "LEGACY_COMMENT"),
                    ("LEGACY_REPLY", "LEGACY_REPLY"),
                    ("LEGACY_THREAD", "LEGACY_THREAD"),
                ],
                default="LEGACY_COMMENT",
                max_length=144,
                null=True,
            ),
        ),
    ]
