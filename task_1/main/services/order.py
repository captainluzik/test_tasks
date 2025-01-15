from task_1.main.models import Order, Cart, PaymentMethod, ShippingMethod
from django.contrib.auth.models import User
from django_q.tasks import async_task
from .payment import PaymentGateway
from django.conf import settings


class OrderService:

    @staticmethod
    def create_order(
            user: User,
            cart: Cart,
            payment_method: PaymentMethod,
            shipping_method: ShippingMethod
    ) -> Order:
        total_price = cart.calculate_total_price() + shipping_method.price \
            if hasattr(shipping_method, 'price') else cart.calculate_total_price()

        order = Order.objects.create(
            user=user,
            cart=cart,
            total_price=total_price,
            status='pending',
            shipping_method=shipping_method,
            payment_method=payment_method
        )

        p = PaymentGateway(
            settings.PAYMENT_BASE_URL,
            "https://our_service.url",
            settings.PAYMENT_API_KEY
        )
        payment_url = p.create_payment(order.total_price, order.pk)

        return order, payment_url

    @staticmethod
    def send_order_to_third_party(order: Order) -> None:
        async_task('main.tasks.create_shipment', order.pk)

    @staticmethod
    def update_order_status(order: Order, status: str) -> None:
        order.status = status
        order.save()
        OrderService._notify_user(order.user, f"Order status changed to {status}")

    @staticmethod
    def update_tracking_info(order: Order, tracking_number: str) -> None:
        order.tracking_number = tracking_number
        order.save()
        OrderService._notify_user(order.user, f"Tracking number: {tracking_number}")

    @staticmethod
    def send_tracking_info(order: Order, message: str) -> None:
        OrderService._notify_user(order.user, f"Tracking number: {order.tracking_number}, {message}")

    @staticmethod
    def _notify_user(user: User, message):
        async_task('main.tasks.send_notification', user.pk, message)
