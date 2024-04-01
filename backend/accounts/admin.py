from django.contrib import admin

from accounts.models import Notification, User

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'type')

admin.site.register(User)
admin.site.register(Notification, NotificationAdmin)