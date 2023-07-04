# Generated by Django 4.2.1 on 2023-07-03 11:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_remove_profile_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='uid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, null=True),
        ),
    ]
