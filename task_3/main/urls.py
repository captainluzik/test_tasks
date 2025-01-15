from django.urls import path
from .views import WebhookReceiverView

urlpatterns = [
    path('webhook/receive/', WebhookReceiverView.as_view(), name='webhook-receive'),
]