# Generated by Django 3.2.25 on 2024-08-25 13:09

from django.db import migrations, models
import helpers.s3


class Migration(migrations.Migration):

    dependencies = [
        ('streaks', '0011_auto_20240822_0853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streak',
            name='background_picture',
            field=models.ImageField(blank=True, null=True, upload_to=helpers.s3.UploadFileTo('streak', 'streak-background')),
        ),
        migrations.AlterField(
            model_name='streak',
            name='local_background_picture',
            field=models.TextField(blank=True, max_length=64, null=True),
        ),
    ]