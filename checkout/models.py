from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

from products.models import Product

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    active = models.BooleanField(default=True)

    def is_valid(self):
        now = timezone.now()
        return (self.active and 
                self.valid_from <= now <= self.valid_to)

    def calculate_discount(self, total_price):
        if self.is_valid():
            return total_price * (self.discount / 100)
        return 0

    def apply_discount(self, total_price):
        discount = self.calculate_discount(total_price)
        return total_price - discount

    def __str__(self):
        return f"{self.code} - {self.discount}% off"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ]

    PAYMENT_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer')
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='orders'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Shipping Information
    shipping_first_name = models.CharField(max_length=100)
    shipping_last_name = models.CharField(max_length=100)
    shipping_address = models.CharField(max_length=255)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_zip_code = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100)
    
    # Payment Details
    payment_method = models.CharField(
        max_length=20, 
        choices=PAYMENT_CHOICES
    )
    
    # Order Status
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    
    # Coupon and Discount
    coupon = models.ForeignKey(
        Coupon, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL
    )
    discount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0
    )

    @property
    def final_price(self):
        total = sum(item.get_total_price() for item in self.items.all())
        return total - self.discount

    def get_total_cost(self):
        total = sum(item.get_total_price() for item in self.items.all())
        return total - self.discount if self.discount else total

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, 
        related_name='items', 
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
