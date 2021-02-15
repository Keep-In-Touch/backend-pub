# Generated by Django 3.1.2 on 2020-10-12 21:25

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('kit_people', '0007_auto_20201012_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regularity',
            name='week_days',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')], max_length=13, verbose_name='week days'),
        ),
    ]
