from django.db import models
from django.contrib.auth.models import User
from api.products.models import Product

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status_choices = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default="pending")

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_quantity = models.PositiveIntegerField(default=0)

    def calculate_totals(self):
        """Calculate total price and total quantity from order items"""
        self.total_price = sum(item.total_price() for item in self.items.all()) + self.shipping_price
        self.total_quantity = sum(item.quantity for item in self.items.all())
        self.save()

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        """Calculate total price for the item"""
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"
