from .models import Event, WebhookClient
from .services import WebhookService


def send_webhook(event_id, client_id):
    event = Event.objects.get(id=event_id)
    client = WebhookClient.objects.get(id=client_id)
    WebhookService.send_event(event, client)
