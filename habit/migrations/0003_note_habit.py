# Generated by Django 3.1 on 2020-10-19 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('habit', '0002_auto_20201019_2323'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='habit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='habit.habit', verbose_name='habit'),
            preserve_default=False,
        ),
    ]