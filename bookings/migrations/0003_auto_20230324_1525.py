# Generated by Django 3.1.5 on 2023-03-24 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_auto_20230324_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='floor',
            name='identifier',
            field=models.CharField(max_length=25),
        ),
    ]
