# Generated by Django 4.1.7 on 2023-03-02 08:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='check_in',
            field=models.DateField(default=datetime.datetime(2023, 3, 2, 8, 28, 47, 980550, tzinfo=datetime.timezone.utc), verbose_name='check-in'),
        ),
    ]