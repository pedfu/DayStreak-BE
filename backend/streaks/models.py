import uuid

from django.db import models

class Badge(models.Model):
    UPLOAD_TO = 'badge'
    name = models.TextField(
        max_length=265,
        null=False,
        blank=False,
    )

    icon = models.ImageField(
        upload_to='badge-icon/',
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
    UPLOAD_TO = 'streak'
    class StreakStatus(models.TextChoices):
        ACTIVE = 'active',
        DAY_COMPLETED = 'day_completed',
        DONE = 'done',
        PAUSED = 'paused',
        DELETED = 'deleted',
    
    name = models.TextField(
        max_length=265,
        null=False,
        blank=False,
    )
    
    duration_days = models.IntegerField(
        null=True,
        blank=False,
    )
    
    min_time_per_day = models.IntegerField(
        null=False,
        blank=False,
        default=0
    )

    end_date = models.DateField(
        null=True,
        blank=False
    )

    goal_deadline = models.DateField(
        null=True,
        blank=False
    )

    status = models.CharField(
        max_length=16,
        choices=StreakStatus.choices,
        default=StreakStatus.ACTIVE
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
    
    local_background_picture = models.TextField(
        max_length=64,
        null=True,
        blank=True,
    )
    
    background_picture = models.ImageField(
        upload_to='streak-background/',
        null=True,
        blank=True,
    )

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
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
    class UserStreakStatus(models.TextChoices):
        DAY_GONE = 'day_done',
        PENDING = 'pending',
        STREAK_OVER = 'streak_over',

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
    
    status = models.CharField(
        max_length=16,
        choices=UserStreakStatus.choices,
        default=UserStreakStatus.PENDING
    )
    
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )

class StreakTrack(models.Model):
    minutes = models.IntegerField(
        null=False,
        blank=False,
    )

    date = models.DateField(
        null=True,
        blank=True,
    )

    user_streak = models.ForeignKey(
        UserStreak,
        related_name='track_user_streak',
        on_delete=models.CASCADE,
    )

    description = models.TextField(
        max_length=1024,
        null=True,
        blank=True,
    )