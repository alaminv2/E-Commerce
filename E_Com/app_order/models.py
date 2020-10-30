from django.db import models
from django.conf import settings
from app_shop.models import Product

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="cart_user")
    item = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_item")
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.quantity} x {self.item}'

    def cart_total(self):
        return format(float(self.quantity * self.item.price), '0.2f')


class Order(models.Model):
    orderitems = models.ManyToManyField(Cart)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="order_user")
    ordered = models.BooleanField(default=False)

    order_id = models.CharField(max_length=264, blank=True, null=True)
    payment_id = models.CharField(max_length=200, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)

    def order_total(self):
        total = 0
        for obj in self.orderitems.all():
            total += float(obj.cart_total())
        return format(total, '0.2f')
