# Generated by Django 4.1 on 2023-10-25 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0096_remove_author_openalex_id_author_openalex_ids"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="linkedin_data",
        ),
        migrations.AddField(
            model_name="author",
            name="linkedin_data",
            field=models.JSONField(blank=True, null=True),
        ),
    ]
