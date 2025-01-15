from .services import ShippingGateway
from django.conf import settings
from .models import Cart
from django.contrib.auth.models import User


def create_shipment(order_id: int):
    sg = ShippingGateway(
        settings.SHIPPING_BASE_URL,
        "https://our_service.url",
        settings.SHIPPING_API_KEY
    )
    sg.create_shipping(order_id, "Some address")


def send_notification(user_id: int, message: str):
    # For example, we can send notification via email
    pass


def delete_carts_schedule():
    # This function should be called by a cron job - every day at 00:00
    users = User.objects.all()
    for user in users:
        if not user.is_authenticated:
            cart = Cart.objects.filter(user=user, status='open').first()
            if cart:
                cart.delete()
