from django.contrib import admin
from . import models

@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'subscribed_to', 'created_at')
    search_fields = ('subscriber__username', 'subscribed_to__username')

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_at')
    search_fields = ('author__username',)

@admin.register(models.Booking)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'master', 'start_time', 'end_time')
    #search_fields = ('author__username',)