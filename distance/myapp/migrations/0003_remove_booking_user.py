# Generated by Django 4.2.3 on 2023-07-15 05:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_booking_booking_id_booking_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='user',
        ),
    ]
