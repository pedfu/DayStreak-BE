from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.utils.crypto import get_random_string
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from accounts.models import *
from helpers.email import send_signup_confirmation_email

class SignUpUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.set_password(validated_data['password'])
        instance.role = 'default'
        instance.email_confirmation_token = get_random_string(length=32)
        instance.email_confirmed = False
        instance.save()

        # ask for email confirmation
        send_signup_confirmation_email(validated_data['email'], validated_data['first_name'], validated_data['last_name'], validated_data['username'], instance.email_confirmation_token)

        return validated_data
    
    class Meta:
        model = User
        fields = '__all__'

class LoginUserSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = '__all__'

class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = '__all__'

class UserResSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'username', 'role', 'profile_picture', 'uuid', 'max_streak', 'groups', 'user_permissions', 'badges')

class TokenUserSerializer(serializers.ModelSerializer):
    user = UserResSerializer()

    class Meta:
        model = Token
        fields = ('key', 'user')

class UserBadgesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ('id', 'name', 'icon', 'rarity')

class UserProfilePictureSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=True)

    def validate(self, attrs):
        if not attrs.get('profile_picture'):
            return ValidationError({'profile_picture': _('This field is required.')})
        return self.initial_data
        
    def update(self, instance, validated_data):
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()
        return instance
      
    class Meta:
        model = User
        fields = ['profile_picture']  
        
class NotificationsSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        title = self.initial_data.get('title')
        message = self.initial_data.get('message')

        if not title:
            raise ValidationError({'title': _('This field is required.')}) 
        if not message:
            raise ValidationError({'message': _('This field is required.')}) 
        return self.initial_data

    def create(self, validated_data):
        user = self.context['user']
        type = validated_data.get('type') or 'default'

        badge = None
        streak = None
        if (validated_data.get('badge') != None):
            badge = Badge.objects.filter(id=validated_data.get('badge'))
        if (validated_data.get('streak') != None):
            streak = Streak.objects.filter(id=validated_data.get('streak'))

        notification = Notification.objects.create(
            title=validated_data.get('title'), 
            message=validated_data.get('message'),
            read=False,
            type=type,
            badge=badge,
            streak=streak,
            user=user
        )
        return notification

    class Meta:
        model = Notification
        fields = ('id', 'title', 'message', 'type', 'read', 'badge', 'streak', 'created_at')