from django.test import TestCase

# Создайте ваши тесты здесь

import datetime
from django.utils import timezone
from shop.forms import SaleForm
from shop.models import Sale, Product, Seller


class FormTest(TestCase):
    """
    Тестируется:
    - Возможность покупки товара через форму,
    - Невозможность покупки товара больше, чем есть на складе,
    - Невозможность покупки товара, которого нет у продавца,
    - Проверка того, что максимально возможное количество для покупки (на стороне клиента, в html форме) устанавливается верно,
    - Проверка того, что выбор продавцов в форме у соответсвующего товара правильный и совпадает с данными в БД.
    """
    fixtures = ['fixtures/seller.json', 'fixtures/product.json', 'fixtures/sale.json']

    def test_create_new_sale_in_form(self):
        seller = Seller.objects.get(pk=8)
        product = Product.objects.get(pk=7)
        sellers_qs = Seller.objects.filter(product=product.pk)

        form_data = {'amount': 1, 'product_id': product.pk, 'sellers': seller}
        form = SaleForm(data=form_data, sellers_qs=sellers_qs, max_amount=product.amount)
        self.assertTrue(form.is_valid())

    def test_amount_more_then_in_stock(self):
        seller = Seller.objects.get(pk=8)
        product = Product.objects.get(pk=7)
        sellers_qs = Seller.objects.filter(product=product.pk)
        form_data = {'amount': product.amount + 1, 'product_id': product.pk, 'sellers': seller}
        form = SaleForm(data=form_data, sellers_qs=sellers_qs, max_amount=product.amount)
        self.assertFalse(form.is_valid())

    def test_wrong_seller(self):
        seller = Seller.objects.get(pk=7)
        product = Product.objects.get(pk=7)
        sellers_qs = Seller.objects.filter(product=product.pk)
        form_data = {'amount': product.amount, 'product_id': product.pk, 'sellers': seller}
        form = SaleForm(data=form_data, sellers_qs=sellers_qs, max_amount=product.amount)
        self.assertFalse(form.is_valid())

    def test_max_value_to_integerfield_is_set_successfully(self):
        seller = Seller.objects.get(pk=8)
        product = Product.objects.get(pk=7)
        sellers_qs = Seller.objects.filter(product=product.pk)

        form_data = {'amount': 1, 'product_id': product.pk, 'sellers': seller}
        form = SaleForm(data=form_data, sellers_qs=sellers_qs, max_amount=product.amount)

        self.assertEqual(form.fields['amount'].max_value, product.amount)
        self.assertEqual(form.fields['amount'].widget.attrs['max'], product.amount)

    def test_sellers_queryset_is_set_successfully(self):
        seller = Seller.objects.get(pk=8)
        product = Product.objects.get(pk=7)
        sellers_qs = Seller.objects.filter(product=product.pk)

        form_data = {'amount': 1, 'product_id': product.pk, 'sellers': seller}
        form = SaleForm(data=form_data, sellers_qs=sellers_qs, max_amount=product.amount)

        for f, q in zip(form.fields['sellers'].queryset, sellers_qs):
            self.assertEqual(f, q)
