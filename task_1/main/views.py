from rest_framework import viewsets, permissions, status, views
from rest_framework.response import Response
from .models import Product, Cart, CartItem, Discount, Order, PaymentMethod, ShippingMethod, ShipmentDetails
from .serializers import (
    CartSerializer,
    CartItemSerializer,
    DiscountSerializer,
    OrderSerializer,
    PaymentMethodSerializer,
    ShippingMethodSerializer
)
from .services import CartService, OrderService


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def close_cart(self, request):
        cart = self.get_object()
        CartService.close_cart(cart)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        cart = CartService.get_cart(self.request.user)
        product_id = self.request.data.get('product')
        product = Product.objects.get(id=product_id)
        quantity = self.request.data.get('quantity')
        CartService.add_item_to_cart(cart, product, quantity)

    def perform_update(self, serializer):
        cart_item = self.get_object()
        new_quantity = self.request.data.get('quantity')
        if new_quantity:
            CartService.change_item_quantity(cart_item, new_quantity)
        discount_id = self.request.data.get('discount')
        if discount_id:
            discount = Discount.objects.get(id=discount_id)
            CartService.apply_discount_to_cart(cart_item.cart, discount)

    def perform_destroy(self, instance):
        CartService.remove_item_from_cart(instance)


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [permissions.IsAuthenticated]


class ShippingMethodViewSet(viewsets.ModelViewSet):
    queryset = ShippingMethod.objects.all()
    serializer_class = ShippingMethodSerializer
    permission_classes = [permissions.IsAuthenticated]


class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        cart_id = request.data.get('cart')
        payment_method_id = request.data.get('payment_method')
        shipping_method_id = request.data.get('shipping_method')
        address = request.data.get('address')
        phone = request.data.get('phone')
        email = request.data.get('email')
        notes = request.data.get('notes', '')

        try:
            cart = Cart.objects.get(id=cart_id, user=request.user)
            payment_method = PaymentMethod.objects.get(id=payment_method_id)
            shipping_method = ShippingMethod.objects.get(id=shipping_method_id)

            order, payment_url = OrderService.create_order(request.user, cart, payment_method, shipping_method)
            CartService.close_cart(cart)

            ShipmentDetails.objects.create(
                order=order,
                address=address,
                phone=phone,
                email=email,
                notes=notes
            )
            serializer = self.get_serializer(order)
            return Response({"order": serializer.data, "payment_url": payment_url}, status=status.HTTP_201_CREATED)

        except Cart.DoesNotExist:
            return Response({"error": "Cart not found."},
                            status=status.HTTP_404_NOT_FOUND)
        except PaymentMethod.DoesNotExist:
            return Response({"error": "Payment method not found."}, status=status.HTTP_404_NOT_FOUND)
        except ShippingMethod.DoesNotExist:
            return Response({"error": "Shipping method not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PaymentCallbackView(views.APIView):
    permission_classes = [permissions.AllowAny]  # This should be changed to a more secure permission

    def post(self, request):
        order_id = request.data.get('order_id')
        payment_status = request.get('payment_status')

        order = Order.objects.filter(id=order_id).first()
        if not order:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        if payment_status == 'success':
            OrderService.update_order_status(order, 'paid')
            OrderService.send_order_to_third_party(order)
            return Response({"message": "Payment successful."}, status=status.HTTP_200_OK)


class ShipmentCallbackView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        order_id = request.data.get('order_id')
        tracking_number = request.data.get('tracking_number')
        shipment_details = request.data.get('shipment_details')

        order = Order.objects.filter(id=order_id).first()
        if not order:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        OrderService.update_tracking_info(order, tracking_number) if not order.tracking_number else None
        OrderService.send_tracking_info(order, shipment_details)
        return Response({"message": "Tracking number updated."}, status=status.HTTP_200_OK)
