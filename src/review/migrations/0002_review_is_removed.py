# Generated by Django 2.2 on 2022-04-27 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='is_removed',
            field=models.BooleanField(default=False),
        ),
    ]
