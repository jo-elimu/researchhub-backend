# Generated by Django 2.2 on 2021-12-17 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jupyter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jupytersession',
            name='token',
            field=models.CharField(default=1, max_length=64),
            preserve_default=False,
        ),
    ]
