# Generated by Django 3.2.25 on 2024-04-02 02:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streaks', '0002_auto_20240401_0746'),
    ]

    operations = [
        migrations.RenameField(
            model_name='streaktrack',
            old_name='duration_days',
            new_name='duration',
        ),
    ]
