# Generated by Django 4.2.1 on 2023-06-22 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_booking_remark'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='drop_city',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='booking',
            name='pickup',
            field=models.CharField(default='', max_length=100),
        ),
    ]
