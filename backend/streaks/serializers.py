from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.utils import timezone
from datetime import timedelta

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

        category, _ = StreakCategory.objects.get_or_create(name=category_name, user=user)
        streak, _ = Streak.objects.get_or_create(name=streak_name, duration_days=streak_duration_days, description=streak_description, created_by=user)
        user_streak, _ = UserStreak.objects.get_or_create(user=user, streak=streak, category=category)

        return user_streak
    
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

    class Meta:
        model = UserStreak
        fields = ('id', 'name', 'description', 'duration_days', 'user_streak_id', 'category')

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
        return 'https://img.freepik.com/free-vector/flat-design-collage-background_23-2149545328.jpg?w=1060&t=st=1712496146~exp=1712496746~hmac=a8ec74df525d6564e54e06c786bcada19a7a072fda14134f2f7deae5c9ac36fa'
        # return instance.streak.background_picture

    def get_max_streak(self, instance: UserStreak):
        # FAZER DPS
        return 1

    class Meta:
        model = UserStreak
        fields = ('id', 'name', 'category', 'duration_days', 'description', 'created_by', 'user_streak_id', 'status', 'background_picture', 'max_streak')

class UserStreakCountSerializer(serializers.ModelSerializer):
    id = SerializerMethodField()
    name = SerializerMethodField()
    category = SerializerMethodField()
    user_streak_id = SerializerMethodField()
    description = SerializerMethodField()
    duration_days = SerializerMethodField()
    day_streak = SerializerMethodField()
    tracks = SerializerMethodField()

    def validate(self, attrs):
        streak_id = self.initial_data.get('streak_id')
        duration = self.initial_data.get('duration')
        start_date = self.initial_data.get('start_date')
        end_date = self.initial_data.get('end_date')

        if not streak_id:
            raise ValidationError({'streak_id': _('This field is required.')}) 
        if not duration:
            raise ValidationError({'duration': _('This field is required.')}) 
        if not start_date:
            raise ValidationError({'start_date': _('This field is required.')}) 
        if not end_date:
            raise ValidationError({'end_date': _('This field is required.')}) 
        
        return self.initial_data

    def create(self, validated_data):
        user = self.context['user']
        streak_id = validated_data['streak_id']
        duration = validated_data['duration']
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']
        description = validated_data['description']

        streak = Streak.objects.filter(id=streak_id).first()
        user_streak = UserStreak.objects.filter(streak=streak, user=user).first()
        # if user_streak:
            # track = StreakTrack.objects.create(
            #     duration=duration,
            #     start_datetime=start_date,
            #     end_datetime=end_date,
            #     user_streak=user_streak,
            #     description=description
            # )
        return user_streak
    
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
        tracks = StreakTrack.objects.filter(user_streak=instance).order_by('-start_datetime')
        current_date = tracks.first().start_datetime.date()
        streak_count = 1 if len(tracks) > 0 else 0

        for track in tracks[1:]:
            if track.start_datetime.date() == current_date:
                continue
            if current_date - track.start_datetime.date() == timedelta(days=1):
                streak_count += 1
            else:
                break
        return streak_count
    
    def get_tracks(self, instance: UserStreak):
        streak_serializer = StreakTrackSerializer(data=StreakTrack.objects.filter(user_streak=instance).order_by('-start_datetime'), many=True)
        if streak_serializer.is_valid():
            return streak_serializer.data
        else:
            return []

    class Meta:
        model = UserStreak
        fields = ('id', 'name', 'description', 'duration_days', 'user_streak_id', 'category', 'day_streak', 'tracks')

class StreakTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreakTrack
        fields = ('id', 'start_datetime', 'end_datetime', 'duration', 'description')

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
        tracks = StreakTrack.objects.filter(user_streak=instance).order_by('-start_datetime')
        if not tracks.first():
            return 0
        current_date = tracks.first().start_datetime.date()
        streak_count = 1 if len(tracks) > 0 else 0

        for track in tracks[1:]:
            if track.start_datetime.date() == current_date:
                continue
            if current_date - track.start_datetime.date() == timedelta(days=1):
                streak_count += 1
            else:
                break
        return streak_count
    
    def get_tracks(self, instance: UserStreak):
        streak_serializer = StreakTrackSerializer(data=StreakTrack.objects.filter(user_streak=instance).order_by('-start_datetime'), many=True)
        if streak_serializer.is_valid():
            return streak_serializer.data
        else:
            return []

    class Meta:
        model = UserStreak
        fields = ('id', 'name', 'description', 'duration_days', 'user_streak_id', 'category', 'day_streak', 'tracks')