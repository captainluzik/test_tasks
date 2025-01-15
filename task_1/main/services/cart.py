from task_1.main.models import Cart, Product, CartItem, Discount
from .discount import DiscountService
from django.contrib.auth.models import User
from django.core.cache import cache


class CartService:

    @staticmethod
    def create_cart(user: User) -> Cart:
        return Cart.objects.create(user=user)

    @staticmethod
    def get_cart(user: User) -> Cart:
        cart = cache.get(f'cart_{user.id}')
        if not cart:
            cart = Cart.objects.filter(user=user, status='open').first()
            cache.set(f'cart_{user.id}', cart, timeout=5 * 60)
        return cart

    @staticmethod
    def close_cart(cart: Cart) -> None:
        cart.delete()

    @staticmethod
    def add_item_to_cart(cart: Cart, product: Product, quantity: int) -> None:
        CartItem.objects.create(cart=cart, product=product, quantity=quantity, price=product.price)
        cache.delete(f'cart_{cart.user.id}')

    @staticmethod
    def change_item_quantity(cart_item: CartItem, new_quantity: int) -> None:
        cart_item.quantity = new_quantity
        cart_item.save()
        cache.delete(f'cart_{cart_item.cart.user.id}')

    @staticmethod
    def remove_item_from_cart(cart_item: CartItem) -> None:
        cart_item.delete()
        cache.delete(f'cart_{cart_item.cart.user.id}')

    @staticmethod
    def apply_discount_to_cart(cart: Cart, discount: Discount) -> None:
        DiscountService().apply_discount_to_cart(cart, discount)
        cache.delete(f'cart_{cart.user.id}')
