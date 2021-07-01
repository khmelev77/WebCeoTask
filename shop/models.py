from django.conf import settings
from django.db import models
from django.utils import timezone

class Seller(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Product(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

class Sale(models.Model):
    date_of_sale = models.DateTimeField(default=timezone.now)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()