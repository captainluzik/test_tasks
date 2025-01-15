from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Product Name')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Product Price')
    stock = models.PositiveIntegerField(verbose_name='Product Stock')

    def __str__(self):
        return f"{self.name} | {self.price}$ | in stock: {self.stock}"

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        indexes = [
            models.Index(fields=['name', 'price']),
        ]


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    status = models.CharField(max_length=50, choices=[('open', 'Open'), ('closed', 'Closed')], default='open',
                              verbose_name='Cart Status')

    def __str__(self):
        return f"Cart of {self.user.username}"

    def calculate_total_price(self):
        return sum([item.price for item in self.items.all()])

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Cart', related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')
    quantity = models.PositiveIntegerField(verbose_name='Product Quantity')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Product Price (may be with discount)')

    def __str__(self):
        return f"{self.product.name} | {self.quantity} items"

    def _calculate_price(self):
        return self.product.price * self.quantity

    def save(self, *args, **kwargs):
        self.price = self._calculate_price()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'


class Discount(models.Model):
    name = models.CharField(max_length=255, verbose_name='Discount Name')
    discount_type = models.CharField(max_length=50, choices=[('percent', 'Percent'), ('fixed', 'Fixed')],
                                     verbose_name='Discount Type')
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Discount Value')
    apply_to = models.ManyToManyField(Product, verbose_name='Apply to Products', related_name='discounts')

    def __str__(self):
        return f"{self.name} | {self.discount_type} | {self.value}"

    class Meta:
        verbose_name = 'Discount'
        verbose_name_plural = 'Discounts'


class CartDiscount(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Cart')
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, verbose_name='Discount')
    applied_at = models.DateTimeField(auto_now_add=True, verbose_name='Applied At')

    def __str__(self):
        return f"{self.discount.name} | {self.cart.user.username}"

    class Meta:
        verbose_name = 'Cart Discount'
        verbose_name_plural = 'Cart Discounts'


class ShippingMethod(models.Model):
    name = models.CharField(max_length=255, verbose_name='Shipping Method Name')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Shipping Method Price')

    def __str__(self):
        return f"{self.name} | {self.price}$"

    class Meta:
        verbose_name = 'Shipping Method'
        verbose_name_plural = 'Shipping Methods'


class PaymentMethod(models.Model):
    name = models.CharField(max_length=255, verbose_name='Payment Method Name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Payment Method'
        verbose_name_plural = 'Payment Methods'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Cart')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total Price')
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('created', 'Created'), ('paid', 'Paid'),
                                                      ('shipped', 'Shipped')], verbose_name='Order Status')
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.SET_NULL, verbose_name='Shipping Method',
                                        null=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, verbose_name='Payment Method',
                                       null=True)
    tracking_number = models.CharField(max_length=255, verbose_name='Tracking Number', null=True, blank=True)


class ShipmentDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Order', related_name='shipment_details')
    address = models.TextField(verbose_name='Shipping Address')
    phone = models.CharField(max_length=50, verbose_name='Phone Number')
    email = models.EmailField(verbose_name='Email Address')
    notes = models.TextField(verbose_name='Notes')

    class Meta:
        verbose_name = 'Shipment Details'
        verbose_name_plural = 'Shipment Details'
