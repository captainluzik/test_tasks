from rest_framework import serializers
from .models import Product, Cart, CartItem, Discount, CartDiscount, Order, PaymentMethod, ShippingMethod, \
    ShipmentDetails


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'price']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'status', 'items', 'total_price']

    def get_total_price(self, obj):
        return obj.calculate_total_price()


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'


class CartDiscountSerializer(serializers.ModelSerializer):
    discount = DiscountSerializer()

    class Meta:
        model = CartDiscount
        fields = ['id', 'cart', 'discount', 'applied_at']


class ShippingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = '__all__'


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'


class ShipmentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentDetails
        fields = ['id', 'address', 'phone', 'email', 'notes']


class OrderSerializer(serializers.ModelSerializer):
    shipping_method = ShippingMethodSerializer()
    payment_method = PaymentMethodSerializer()
    shipment_details = ShipmentDetailsSerializer()

    class Meta:
        model = Order
        fields = '__all__'
