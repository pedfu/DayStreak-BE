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

class StreakSerializer(serializers.Serializer):
    def validate(self, attrs):
        name = self.initial_data.get('name')
        description = self.initial_data.get('description')
        duration_days = self.initial_data.get('duration_days')
        category_name = self.initial_data.get('category_name')

        if not name:
            raise ValidationError({'name': _('This field is required.')}) 
        if not description:
            raise ValidationError({'description': _('This field is required.')}) 
        if not duration_days:
            raise ValidationError({'duration_days': _('This field is required.')}) 
        if not category_name:
            raise ValidationError({'category_name': _('This field is required.')}) 
        
        return self.initial_data

    def create(self, validated_data):
        user = self.context['user']
        streak_name = validated_data.get('name')
        streak_description = validated_data.get('description')
        streak_duration_days = validated_data.get('duration_days')
        category_name = validated_data.get('category_name')

        category = StreakCategory.objects.get_or_create(name=category_name, user=user)
        streak = Streak.objects.create(name=streak_name, duration_days=streak_duration_days, description=streak_description, created_by=user)
        user_streak = UserStreak.objects.create(user=user, streak=streak, category=category)

        return self.__class__(user_streak)
    
    class Meta:
        fields = '__all__'

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