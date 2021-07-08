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
from .utils import check_seller_exist, check_product_exist

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
        initial.update({'amount': 1, 'product_id': self.kwargs['product_id']})
        return initial

    def dispatch(self, request, *args, **kwargs):
        product = check_product_exist(self.kwargs['product_id'])
        if not product:
            messages.add_message(request, messages.ERROR, 'Нужный товар не был найден, возможно он был удален.')
            return redirect('product_list')

        sellers_qs = check_seller_exist(product)
        if not sellers_qs:
            messages.add_message(request, messages.ERROR, 'Продавцы для данной позиции отсутствуют в базе данных.')
            return redirect('product_list')

        self.kwargs['product'] = product
        self.kwargs['sellers_qs'] = sellers_qs

        return super(ProductDetail, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        form_kwargs = super(ProductDetail, self).get_form_kwargs()
        form_kwargs['sellers_qs'] = self.kwargs['sellers_qs']
        form_kwargs['max_amount'] = self.kwargs['product'].amount
        return form_kwargs

    def form_valid(self, form):
        product = self.kwargs['product']

        if not product:
            form.add_error(None, 'Нужный товар не был найден, возможно он был удален.')
            return super(ProductDetail, self).form_invalid(form)

        if product.amount < form.cleaned_data['amount']:
            form.add_error('amount', 'Товар в нужном кол-ве отсутсвтует на складе.')
            return super(ProductDetail, self).form_invalid(form)

        form.save()
        return super(ProductDetail, self).form_valid(form)

    def get_context_data(self, **kwargs):
        product = self.kwargs['product']
        # Если и вернется None, то в шаблоне отобразиться надпись, что товар не был найден в базе данных.
        context = super().get_context_data(**kwargs)
        context["product"] = product
        return context


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