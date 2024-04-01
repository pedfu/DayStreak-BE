import uuid

from django.db import models
from helpers.s3 import UploadFileTo

class Badge(models.Model):
    UPLOAD_TO = 'badge'
    name = models.TextField(
        max_length=265,
        null=False,
        blank=False,
    )

    icon = models.ImageField(
        upload_to=UploadFileTo(UPLOAD_TO, 'badge-icon'),
        null=True,
        blank=True,
    )

    rarity = models.ForeignKey(
        'streaks.BadgeRarity',
        related_name='badge_rarity',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )

class BadgeRarity(models.Model):
    rarity_order = models.IntegerField(
        null=False,
        blank=False,
    )

    name = models.TextField(
        max_length=24,
        null=False,
        blank=False,
    )


class Streak(models.Model):
    name = models.TextField(
        max_length=265,
        null=False,
        blank=False,
    )
    
    duration_in_seconds = models.IntegerField(
        null=False,
        blank=False,
    )

    description = models.TextField(
        max_length=1024,
        null=False,
        blank=False,
    )

    created_by = models.ForeignKey(
        'accounts.User',
        related_name='created_by_user',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

class StreakCategory(models.Model):
    name = models.TextField(
        max_length=32,
        null=False,
        blank=False,
    )

    user = models.ForeignKey(
        'accounts.User',
        related_name='category_user',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

class UserStreak(models.Model):

    user = models.ForeignKey(
        'accounts.User',
        related_name='user_streak',
        on_delete=models.CASCADE,
    )

    streak = models.ForeignKey(
        Streak,
        related_name='user_streak',
        on_delete=models.CASCADE,
    )
    
    category = models.ForeignKey(
        StreakCategory,
        related_name='streak_category',
        on_delete=models.CASCADE,
    )

class StreakTrack(models.Model):
    duration_in_seconds = models.IntegerField(
        null=False,
        blank=False,
    )

    start_datetime = models.DateTimeField(
        null=True,
        blank=True,
    )

    end_datetime = models.DateTimeField(
        null=True,
        blank=True,
    )

    streak = models.ForeignKey(
        UserStreak,
        related_name='track_user_streak',
        on_delete=models.CASCADE,
    )

    # streak = models.ForeignKey(
    #     Streak,
    #     related_name='streak_track',
    #     on_delete=models.CASCADE,
    # )

    # user = models.ForeignKey(
    #     'accounts.User',
    #     related_name='streak_track_user',
    #     on_delete=models.CASCADE,
    # )

    description = models.TextField(
        max_length=1024,
        null=False,
        blank=False,
    )