from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CartViewSet,
    CartItemViewSet,
    DiscountViewSet,
    ShippingMethodViewSet,
    PaymentMethodViewSet,
    OrderViewSet,
    PaymentCallbackView,
    ShipmentCallbackView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()

router.register(r'carts', CartViewSet, basename='cart')
router.register(r'cart-items', CartItemViewSet, basename='cart-item')
router.register(r'discounts', DiscountViewSet, basename='discount')
router.register(r'shipping-methods', ShippingMethodViewSet, basename='shipping-method')
router.register(r'payment-methods', PaymentMethodViewSet, basename='payment-method')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('payments/callback', PaymentCallbackView.as_view(), name='payment-callback'),
    path('shipments/callback', ShipmentCallbackView.as_view(), name='shipment-callback'),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Order API",
        default_version='v1',
        description="API for managing orders, carts, and discounts",
    ),
    public=True,
)

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
