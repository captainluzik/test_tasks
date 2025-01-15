from task_1.main.models import Cart, Discount, CartDiscount
from .adstracts import DiscountStrategy


class PercentDiscountStrategy(DiscountStrategy):

    def apply_discount(self, cart: Cart, discount: Discount) -> None:
        for item in cart.items.all():
            if discount.apply_to.filter(id=item.product.id).exists():
                item.price = item.price * (1 - discount.value / 100)
                item.save()


class FixedDiscountStrategy(DiscountStrategy):

    def apply_discount(self, cart: Cart, discount: Discount) -> None:
        for item in cart.items.all():
            if discount.apply_to.filter(id=item.product.id).exists():
                item.price = item.price - discount.value
                item.save()


class DiscountService:

    def __init__(self) -> None:
        self.strategies = {
            'percent': PercentDiscountStrategy(),
            'fixed': FixedDiscountStrategy()
        }

    def apply_discount_to_cart(self, cart: Cart, discount: Discount) -> None:
        strategy = self.strategies.get(discount.discount_type)
        if strategy:
            strategy.apply_discount(cart, discount)
            CartDiscount.objects.create(cart=cart, discount=discount)
        else:
            raise ValueError('Unknown discount type')
