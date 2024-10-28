from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.utils import timezone

from streaks.models import Badge, Streak

import uuid
import os

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, username, password):
        if not email:
            raise ValueError('User must have email address')
        if not password:
            raise ValueError('User must have a password')
        if not first_name:
            raise ValueError('User must have a first name')
        if not last_name:
            raise ValueError('User must have a last name')
        
        user_obj = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

def user_profile_picture_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    new_filename = f"profile-picture-{instance.uuid}{extension}"
    return f"profile_pictures/{new_filename}"

class User(AbstractBaseUser, PermissionsMixin):
    UPLOAD_TO = 'user'
    USERNAME_FIELD = 'username'

    class UserRole(models.TextChoices):
        ADMIN = 'admin',
        DEFAULT = 'default',
        PREMIUM = 'premium',
    
    objects = UserManager()
    
    email = models.EmailField(max_length=255, unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False) 
    username = models.CharField(max_length=255, blank=False, null=False, unique=True) 
    
    @property
    def is_staff(self):
        return self.role == 'admin'
    
    @property
    def is_superuser(self):
        return self.role == 'admin'
    
    # @property
    # def has_module_perms(self):
    #     return self.role == 'admin'
    
    groups = models.ManyToManyField(
        Group,
        blank=True,
        null=True,
        related_name='user_groups'
    )

    # For user_permissions field
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        null=True,
        related_name='user_permissions'
    )
    
    role = models.CharField(
        max_length=16,
        choices=UserRole.choices,
        default=UserRole.DEFAULT
    )

    profile_picture = models.ImageField(
        upload_to=user_profile_picture_path,
        null=True,
        blank=True,
    )

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )

    app_version = models.CharField(
        max_length=32,
        null=True,
        blank=True,
    )

    max_streak = models.IntegerField(
        null=True,
    )

    app_language = models.CharField(
        max_length=6,
        null=False,
        blank=False,
        default='EN',
    )

    email_confirmed = models.BooleanField(
        null=False,
        blank=False,
        default=False,
    )

    email_confirmation_token = models.CharField(
        max_length=32,
        null=True,
        blank=True,
    )

    notification_token = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )

    badges = models.ManyToManyField(
        Badge,
        blank=True,
        null=True,
        related_name='user_badges'
    )

    def save(self, *args, **kwargs):
        if self.id:
            old_user = User.objects.get(id=self.id)
            if old_user.profile_picture and old_user.profile_picture != self.profile_picture:
                old_user.profile_picture.delete(save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class Notification(models.Model):
    class NotificationType(models.TextChoices):
        DEFAULT = 'default',
        CONFIRM = 'confirm',

    title = models.CharField(
        max_length=265,
        null=False,
        blank=False,
    )

    message = models.CharField(
        max_length=1024,
        null=True,
        blank=True,
    )

    type = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=NotificationType.choices
    )

    read = models.BooleanField(
        null=False,
        default=False,
    )

    # badge = models.CharField(
    #     null=True,
    #     blank=True,
    # )

    user = models.ForeignKey(
        User,
        related_name='notification_user',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    badge = models.ForeignKey(
        Badge,
        related_name='notification_badge',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    streak = models.ForeignKey(
        Streak,
        related_name='notification_streak',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        null=False,
        default=timezone.now
    )

    updated_at = models.DateTimeField(
        null=True,
        blank=False,
        default=None
    )
