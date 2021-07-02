from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Product, Seller, Sale
from .forms import SaleForm
from django.shortcuts import redirect

class ProductList(TemplateView):
    template_name = "shop/product_list.html"

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        return render(request, self.template_name, {'products': products})

class ProductDetail(TemplateView):
    template_name = "shop/product_detail.html"

    def get(self, request, *args, **kwargs):
        product = Product.objects.filter(pk=kwargs['product_id'])[0]
        sellers_qs = Seller.objects.filter(product=product.pk)

        if not product or not sellers_qs: return redirect('product_list')

        form = SaleForm(initial={'amount': 1, 'product_id': product.pk},
                        sellers_qs=sellers_qs,
                        max_amount=product.amount)
        return render(request, self.template_name, {'product': product, 'form': form})

    def post(self, request, *args, **kwargs):
        product = Product.objects.filter(pk=kwargs['product_id'])[0]
        sellers_qs = Seller.objects.filter(product=product.pk)

        if not product or not sellers_qs: return redirect('product_list')

        form = SaleForm(request.POST, sellers_qs=sellers_qs, max_amount=product.amount)

        if form.is_valid():
            seller = form.cleaned_data['sellers']

            product.amount -= form.cleaned_data['amount']
            product.save()

            Sale.objects.create(seller=seller, product=product, amount_sold=form.cleaned_data['amount'])

            return redirect('product_list')

        return render(request, self.template_name, {'product': product, 'form': form})