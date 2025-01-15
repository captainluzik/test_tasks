import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import json
import hmac
import hashlib
from .models import WebhookClient, Event, WebhookSubscription
from typing import Dict, Any


class EventService:
    @staticmethod
    def generate_event(event_type: str, data: dict, user_id: int = None):
        event = Event.objects.create(event_type=event_type, data=data)

        subscriptions = WebhookSubscription.objects.filter(event_type=event_type)

        if user_id:
            subscriptions = subscriptions.filter(user_id=user_id)

        for subscription in subscriptions:
            WebhookService.send_event(event, subscription.client)


class WebhookService:

    def __make_headers(self, signature: str) -> Dict[str, Any]:
        pass

    def __make_request(self, method: str, url: str, headers: Dict[str, Any], data: Dict[str, Any]) -> requests.Response:
        session = requests.Session()
        retry = Retry(total=5, backoff_factor=1)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)

        match method.lower():
            case 'post':
                response = session.post(url, headers=headers, data=json.dumps(data))
            case _:
                raise ValueError('Method not allowed')
        return response

    def _post(self, client: WebhookClient, headers: Dict[str, Any], data: Dict[str, Any]) -> requests.Response:
        return self.__make_request('post', client.url, headers, data)

    def __make_signature(self, secret_key, data):
        return hmac.new(secret_key.encode(), json.dumps(data).encode(), hashlib.sha256).hexdigest()

    @staticmethod
    def send_event(event: Event, client: WebhookClient) -> requests.Response:
        try:
            payload = {
                'event_type': event.event_type,
                'data': event.data,
                'timestamp': event.created_at.timestamp()
            }

            signature = WebhookService().__make_signature(client.secret, payload)

            headers = WebhookService().__make_headers(signature)

            response = WebhookService()._post(client, headers, payload)

            if response.status_code != 200:
                raise ValueError('Error while sending event')

            return response

        except Exception as e:
            raise ValueError(f'Error while sending event: {e}')
