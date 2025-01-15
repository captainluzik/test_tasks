from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import hmac
import hashlib
import json
from django.conf import settings
from .models import Event


class WebhookReceiverView(APIView):
    def post(self, request):
        try:
            signature = request.headers.get('X-Webhook-Signature')
            if not signature:
                return Response({"error": "Missing signature"}, status=status.HTTP_400_BAD_REQUEST)

            payload = request.body
            expected_signature = hmac.new(
                settings.WEBHOOK_SECRET_KEY.encode(),
                payload,
                hashlib.sha256
            ).hexdigest()

            if not hmac.compare_digest(signature, expected_signature):
                return Response({"error": "Invalid signature"}, status=status.HTTP_401_UNAUTHORIZED)

            data = json.loads(payload)
            event_type = data.get('event_type')
            event_data = data.get('data')

            Event.objects.create(event_type=event_type, data=event_data)

            return Response({"message": "Event received"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
