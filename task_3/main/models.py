from django.db import models


class WebhookClient(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    secret_key = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class WebhookSubscription(models.Model):
    EVENT_TYPES = [
        ('user_updated', 'User Updated'),
        ('task_created', 'Task Created'),
        ('task_updated', 'Task Updated'),
        ('event_created', 'Event Created'),
        ('event_updated', 'Event Updated'),
    ]

    client = models.ForeignKey(WebhookClient, on_delete=models.CASCADE, related_name='subscriptions')
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    user_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.client.name} - {self.event_type}"


class Event(models.Model):
    event_type = models.CharField(max_length=50, choices=WebhookSubscription.EVENT_TYPES)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_type} at {self.created_at}"
