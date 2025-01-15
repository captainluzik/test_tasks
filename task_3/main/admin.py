from django.contrib import admin
from .models import WebhookClient, WebhookSubscription


@admin.register(WebhookClient)
class WebhookClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'is_active', 'created_at')
    search_fields = ('name', 'url')
    list_filter = ('is_active',)


@admin.register(WebhookSubscription)
class WebhookSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('client', 'event_type', 'user_id')
    search_fields = ('client__name', 'event_type')
    list_filter = ('event_type',)
