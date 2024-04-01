from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ModelSerializer, SerializerMethodField


from streaks.models import *

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreakCategory
        fields = '__all__'

class SimplifiedCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StreakCategory
        fields = ('id', 'name')

class StreakSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer()

    def validate(self, attrs):
        attrs = super().validate(attrs)

        # name
        # duration
        # category name
        if not attrs.get('name', False):
            raise ValidationError({'name': _('This field is required.')}) 
        if not attrs.get('duration_in_sec', False):
            raise ValidationError({'duration_in_sec': _('This field is required.')}) 
        if not attrs.get('category_name', False):
            raise ValidationError({'category_name': _('This field is required.')}) 
        
        return attrs

    def create(self, validated_data):
        print('serializer')
        user = self.context['request'].user
        streak_name = validated_data.get('name')
        streak_description = validated_data.get('description')
        streak_duration_in_sec = validated_data.get('duration_in_sec')
        category_name = validated_data.get('category_name')

        category = StreakCategory.objects.get_or_create(name=category_name, user=user)
        streak = Streak.objects.create(name=streak_name, duration_in_seconds=streak_duration_in_sec, description=streak_description, created_by=user)
        user_streak = UserStreak.objects.create(user=user, streak=streak, category=category)

        # FINALIZAR
        return validated_data
    
    class Meta:
        model = Streak
        fields = ('id', 'name', 'duration_in_seconds', 'description', 'created_by', 'category')

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'

class UserStreakSerializer(serializers.ModelSerializer):
    id = SerializerMethodField()
    name = SerializerMethodField()
    category = SimplifiedCategorySerializer()

    def get_id(self, instance: UserStreak):
        return instance.streak.id

    def get_name(self, instance: UserStreak):
        return instance.streak.name

    class Meta:
        model = UserStreak
        fields = ('id', 'name', 'category')