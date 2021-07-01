from django.shortcuts import render
from annoying.decorators import render_to
from .models import Product

@render_to('shop/product_list.html')
def product_list(request):
    products = Product.objects.all()
    return {'products': products}
