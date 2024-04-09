from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.utils.crypto import get_random_string

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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'username', 'role', 'profile_picture', 'uuid', 'max_streak', 'groups', 'user_permissions', 'badges')

class TokenUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Token
        fields = ('key', 'user')

class UserBadgesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ('id', 'name', 'icon', 'rarity')
        
class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'title', 'message', 'type', 'read', 'badge', 'streak')