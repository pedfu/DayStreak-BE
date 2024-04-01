from django.contrib import admin

from streaks.models import Streak, StreakCategory, StreakTrack, UserStreak, Badge, BadgeRarity

class StreakAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_in_seconds')

class StreakCategoryAdmin(admin.ModelAdmin):
    list_display = ('name')

class StreakTrackAdmin(admin.ModelAdmin):
    list_display = ('duration_in_seconds', 'streak')

class UserStreakAdmin(admin.ModelAdmin):
    list_display = ('user', 'streak', 'category')

class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'rarity')

class BadgeRarityAdmin(admin.ModelAdmin):
    list_display = ('name', 'rarity_order')

admin.site.register(Streak, StreakAdmin)
admin.site.register(StreakCategory)
admin.site.register(StreakTrack, StreakTrackAdmin)
admin.site.register(UserStreak, UserStreakAdmin)
admin.site.register(Badge, BadgeAdmin)
admin.site.register(BadgeRarity, BadgeRarityAdmin)