from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.utils import timezone
from datetime import timedelta
import json

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
    id = SerializerMethodField()
    name = SerializerMethodField()
    category = SerializerMethodField()
    user_streak_id = SerializerMethodField()
    description = SerializerMethodField()
    duration_days = SerializerMethodField()
    background_picture = SerializerMethodField()
    local_background_picture = SerializerMethodField()

    def validate(self, attrs):
        background = self.context.get('background') 

        name = self.initial_data.get('name')
        description = self.initial_data.get('description')
        category_id = self.initial_data.get('category_id')

        if not name:
            raise ValidationError({'name': _('This field is required.')}) 
        if not description:
            raise ValidationError({'description': _('This field is required.')}) 
        if not category_id:
            raise ValidationError({'category_id': _('This field is required.')}) 
        # if not background:
        #     raise ValidationError({'background': _('This field is required.')}) 
        
        self.initial_data['background'] = background       
        return self.initial_data

    def create(self, validated_data):
        user = self.context['user']
        streak_name = validated_data.get('name')
        streak_description = validated_data.get('description') or None
        streak_duration_days = validated_data.get('duration_days')
        end_date = validated_data.get('end_date')
        background = validated_data.get('background')
        category_id = validated_data.get('category_id')
        min_time_per_day = validated_data.get('min_time_per_day') or 0
        local_background_picture = validated_data.get('local_background_picture')

        category = StreakCategory.objects.filter(id=category_id).first()
        streak = Streak.objects.create(
            name=streak_name, 
            duration_days=streak_duration_days, 
            description=streak_description, 
            end_date=end_date,
            min_time_per_day=min_time_per_day,
            background_picture=background,
            local_background_picture=local_background_picture,
            created_by=user)
        user_streak = UserStreak.objects.create(user=user, streak=streak, category=category)
        return user_streak
    
    def update(self, instance, validated_data):
        # Update existing streak and user_streak
        instance.streak.name = validated_data.get('name', instance.streak.name)
        instance.streak.description = validated_data.get('description', instance.streak.description)
        instance.streak.duration_days = validated_data.get('duration_days', instance.streak.duration_days)
        instance.streak.background_picture = validated_data.get('background', instance.streak.background_picture)
        instance.streak.local_background_picture = validated_data.get('local_background_picture', instance.streak.local_background_picture)
        
        instance.streak.save()

        # Update the category if provided
        category_id = validated_data.get('category_id')
        if category_id:
            category = StreakCategory.objects.filter(id=category_id).first()
            instance.category = category
        
        instance.save()
        return instance
    
    def get_category(self, obj):
        if 'data' in self.context:
            category_data = self.context['data'].get('category')
            if category_data:
                return category_data
        return SimplifiedCategorySerializer(obj.category).data
    
    def get_id(self, instance: UserStreak):
        return instance.streak.id

    def get_name(self, instance: UserStreak):
        return instance.streak.name

    def get_description(self, instance: UserStreak):
        return instance.streak.description

    def get_duration_days(self, instance: UserStreak):
        return instance.streak.duration_days

    def get_user_streak_id(self, instance: UserStreak):
        return instance.id

    def get_local_background_picture(self, instance: UserStreak):
        return instance.streak.local_background_picture

    def get_background_picture(self, instance: UserStreak):
        background_picture = instance.streak.background_picture or None
        return instance.streak.background_picture.url if hasattr(background_picture, 'url') else background_picture
    
    class Meta:
        model = UserStreak
        fields = ('id', 'name', 'description', 'duration_days', 'user_streak_id', 'category', 'local_background_picture', 'background_picture')

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'

class UserStreakSerializer(serializers.ModelSerializer):
    id = SerializerMethodField()
    name = SerializerMethodField()
    category = SimplifiedCategorySerializer()
    duration_days = SerializerMethodField()

    description = SerializerMethodField()
    created_by = SerializerMethodField()
    user_streak_id = SerializerMethodField()
    status = SerializerMethodField()
    background_picture = SerializerMethodField()
    local_background_picture = SerializerMethodField()
    max_streak = SerializerMethodField()

    def get_id(self, instance: UserStreak):
        return instance.streak.id

    def get_name(self, instance: UserStreak):
        return instance.streak.name

    def get_duration_days(self, instance: UserStreak):
        return instance.streak.duration_days

    def get_description(self, instance: UserStreak):
        return instance.streak.description

    def get_created_by(self, instance: UserStreak):
        return instance.streak.created_by.username

    def get_user_streak_id(self, instance: UserStreak):
        return instance.id

    def get_status(self, instance: UserStreak):
        return instance.status

    def get_background_picture(self, instance: UserStreak):
        background_picture = instance.streak.background_picture or None
        return instance.streak.background_picture.url if hasattr(background_picture, 'url') else background_picture

    def get_local_background_picture(self, instance: UserStreak):
        return instance.streak.local_background_picture

    def get_max_streak(self, instance: UserStreak):
        # FAZER DPS
        return 1

    class Meta:
        model = UserStreak
        fields = ('id', 'name', 'category', 'duration_days', 'description', 'created_by', 'user_streak_id', 'status', 'background_picture', 'local_background_picture', 'max_streak')

class UserStreakCountSerializer(serializers.ModelSerializer):
    id = SerializerMethodField()
    name = SerializerMethodField()
    category = SerializerMethodField()
    duration_days = SerializerMethodField()
    description = SerializerMethodField()
    created_by = SerializerMethodField()
    user_streak_id = SerializerMethodField()
    status = SerializerMethodField()
    background_picture = SerializerMethodField()
    local_background_picture = SerializerMethodField()
    max_streak = SerializerMethodField()
        
    def validate(self, attrs):
        streak_id = self.initial_data.get('streak_id')
        minutes = self.initial_data.get('minutes')

        if not streak_id:
            raise ValidationError({'streak_id': _('This field is required.')}) 
        if not minutes:
            raise ValidationError({'minutes': _('This field is required.')})
        
        return self.initial_data

    def create(self, validated_data):
        user = self.context['user']
        streak_id = validated_data['streak_id']
        minutes = validated_data['minutes']
        date = validated_data.get('date')
        description = validated_data.get('description')

        streak = Streak.objects.filter(id=streak_id).first()
        user_streak = UserStreak.objects.filter(streak=streak, user=user).first()
        if user_streak:
            track = StreakTrack.objects.create(
                minutes=minutes,
                date=date,
                user_streak=user_streak,
                description=description
            )
            track.save()
        return user_streak
    
    def get_status(self, instance: UserStreak):
        return instance.status
    
    def get_category(self, obj):
        if 'data' in self.context:
            category_data = self.context['data'].get('category')
            if category_data:
                return category_data
        return SimplifiedCategorySerializer(obj.category).data
    
    def get_created_by(self, instance: UserStreak):
        return instance.streak.created_by.username
    
    def get_id(self, instance: UserStreak):
        return instance.streak.id

    def get_name(self, instance: UserStreak):
        return instance.streak.name

    def get_description(self, instance: UserStreak):
        return instance.streak.description

    def get_duration_days(self, instance: UserStreak):
        return instance.streak.duration_days

    def get_user_streak_id(self, instance: UserStreak):
        return instance.id

    def get_local_background_picture(self, instance: UserStreak):
        return instance.streak.local_background_picture

    def get_background_picture(self, instance: UserStreak):
        background_picture = instance.streak.background_picture or None
        return instance.streak.background_picture.url if hasattr(background_picture, 'url') else background_picture

    def get_max_streak(self, instance: UserStreak):
        # FAZER DPS
        return 1
    
    class Meta:
        model = UserStreak
        fields = ('id', 'name', 'category', 'duration_days', 'description', 'created_by', 'user_streak_id', 'status', 'background_picture', 'local_background_picture', 'max_streak')
        # fields = ('id', 'name', 'description', 'duration_days', 'user_streak_id', 'category', 'day_streak', 'tracks')

class StreakTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreakTrack
        fields = ('id', 'date', 'minutes', 'description')

class UserStreakDetailsCountSerializer(serializers.ModelSerializer):
    id = SerializerMethodField()
    name = SerializerMethodField()
    category = SerializerMethodField()
    user_streak_id = SerializerMethodField()
    description = SerializerMethodField()
    duration_days = SerializerMethodField()
    day_streak = SerializerMethodField()
    tracks = SerializerMethodField()
    
    def get_category(self, obj):
        if 'data' in self.context:
            category_data = self.context['data'].get('category')
            if category_data:
                return category_data
        return SimplifiedCategorySerializer(obj.category).data
    
    def get_id(self, instance: UserStreak):
        return instance.streak.id

    def get_name(self, instance: UserStreak):
        return instance.streak.name

    def get_description(self, instance: UserStreak):
        return instance.streak.description

    def get_duration_days(self, instance: UserStreak):
        return instance.streak.duration_days

    def get_user_streak_id(self, instance: UserStreak):
        return instance.id
    
    def get_day_streak(self, instance: UserStreak):
        tracks = StreakTrack.objects.filter(user_streak=instance).order_by('-date')
        if not tracks.first():
            return 0
        current_date = tracks.first().date
        streak_count = 1 if len(tracks) > 0 else 0

        for track in tracks[1:]:
            if track.date == current_date:
                continue
            if current_date - track.date == timedelta(days=1):
                streak_count += 1
            else:
                break
        return streak_count
    
    def get_tracks(self, instance: UserStreak):
        streak_serializer = StreakTrackSerializer(data=StreakTrack.objects.filter(user_streak=instance).order_by('-date'), many=True)
        if streak_serializer.is_valid():
            return streak_serializer.data
        else:
            return []

    class Meta:
        model = UserStreak
        fields = ('id', 'name', 'description', 'duration_days', 'user_streak_id', 'category', 'day_streak', 'tracks')

class CategorySerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        name = self.initial_data.get('name')

        if not name:
            raise ValidationError({'name': _('This field is required.')}) 
        return self.initial_data

    def create(self, validated_data):
        user = self.context['user']
        category_name = (validated_data.get('name')).lower()
        category, _ = StreakCategory.objects.get_or_create(name=category_name, user=user)
        return category

    class Meta:
        model = StreakCategory
        fields = ('id', 'name')
