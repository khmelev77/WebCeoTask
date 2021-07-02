from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Product

class ProductList(TemplateView):
    template_name = "shop/product_list.html"

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        return render(request, self.template_name, {'products': products})

class ProductDetail(TemplateView):
    template_name = "shop/product_detail.html"

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['product_id'])
        #products = Product.objects.all()
        return render(request, self.template_name, {'product': product})