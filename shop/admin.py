from django.contrib import admin, auth
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass