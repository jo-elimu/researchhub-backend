# Generated by Django 2.2 on 2021-11-17 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0073_auto_20211022_0126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gatekeeper',
            name='type',
            field=models.CharField(choices=[('ELN', 'ELN'), ('CLIENT_PERMISSIONS', 'CLIENT_PERMISSIONS'), ('JUPYTER', 'JUPYTER')], db_index=True, max_length=128),
        ),
    ]
