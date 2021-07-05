from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Product, Seller, Sale, ProductPriceChange
from .forms import SaleForm
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages

class ProductList(TemplateView):
    template_name = "shop/product_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context


class ProductDetail(FormView):
    form_class = SaleForm
    template_name = "shop/product_detail.html"
    success_url = reverse_lazy('product_list')

    def get_initial(self):
        initial = super(ProductDetail, self).get_initial()
        if self.request.user.is_authenticated:
            initial.update({'amount': 1, 'product_id': self.kwargs['product_id']})
        return initial

    def dispatch(self, request, *args, **kwargs):
        product = self.check_product_exist(self.request, self.kwargs['product_id'])
        if not product: return redirect('product_list')

        sellers_qs = self.check_seller_exist(self.request, product)
        if not sellers_qs: return redirect('product_list')

        self.kwargs['product'] = product
        self.kwargs['sellers_qs'] = sellers_qs

        return super(ProductDetail, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ProductDetail, self).get_form_kwargs()
        kwargs['sellers_qs'] = self.kwargs['sellers_qs']
        kwargs['max_amount'] = self.kwargs['product'].amount
        return kwargs

    def form_valid(self, form):
        product = self.check_product_exist(self.request, form.cleaned_data['product_id'])
        if not product: return redirect('product_list')

        if product.amount >= form.cleaned_data['amount']:
            product.amount -= form.cleaned_data['amount']
            product.save()
        else:
            messages.add_message(self.request, messages.ERROR, 'Товара на складе оказалось недостаточно, возможно кто-то его уже купил.')
            return redirect('product_list')

        Sale.objects.create(seller=form.cleaned_data['sellers'], product=product, amount_sold=form.cleaned_data['amount'], purchase_amount=product.price * form.cleaned_data['amount'])

        return super(ProductDetail, self).form_valid(form)

    def get_context_data(self, **kwargs):
        product = self.check_product_exist(self.request, self.kwargs['product_id'])

        context = super().get_context_data(**kwargs)
        context["product"] = product
        return context


    def check_product_exist(self, request, product_id):
        try:
            product = Product.objects.filter(pk=product_id)[0]
            return product
        except IndexError:
            messages.add_message(request, messages.ERROR, 'Нужный товар не был найден, возможно он был удален.')
            return None

    def check_seller_exist(self, request, product):
        try:
            sellers_qs = Seller.objects.filter(product=product.pk)
            return sellers_qs
        except IndexError:
            messages.add_message(request, messages.ERROR, 'Продавцы для нужного товара не были найдены.')
            return None

class SalesList(LoginRequiredMixin, TemplateView):
    template_name = "shop/sales_list.html"

    def get(self, request, *args, **kwargs):
        sales = Sale.objects.order_by('-date_of_sale')
        p = Paginator(sales, 5)
        page_number = request.GET.get('page')
        p_obj = p.get_page(page_number)
        return render(request, self.template_name, {'page_obj': p_obj})


class PriceChangelog(LoginRequiredMixin, TemplateView):
    template_name = "shop/price_changelog.html"

    def get(self, request, *args, **kwargs):
        product_id = kwargs.pop('product_id')
        sales = ProductPriceChange.objects.filter(product__id=product_id).order_by('date_of_change')

        p = Paginator(sales, 5)
        page_number = request.GET.get('page')
        p_obj = p.get_page(page_number)
        return render(request, self.template_name, {'page_obj': p_obj})


class ProductCreate(CreateView):
    success_url = reverse_lazy('product_list')
    template_name = 'shop/product_create.html'
    model = Product
    fields = ['title', 'description', 'price', 'amount', 'sellers', 'photo']