# Generated by Django 3.1.2 on 2021-03-22 11:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('habit', '0009_auto_20210302_0102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='start_day',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
    ]