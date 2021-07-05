from django.test import TestCase
from django.shortcuts import reverse
from shop.models import ProductPriceChange, Product
import random


class ProductTest(TestCase):
    """
    - Проверка того, что цена товара изменяется благополучно и создается запись в "журнале изменений".
    - Проверка того, что страница '/' возвращает 200 код.
    """
    fixtures = ["fixtures/seller.json", "fixtures/product.json", "fixtures/sale.json"]

    def test_product_price_change(self):
        new_price = random.randint(1, 9999)
        p = Product.objects.get(pk=9)
        p.price = new_price
        p.save()
        prod_price_change_obj = ProductPriceChange.objects.filter(product=p).order_by(
            "-date_of_change"
        )[0]
        self.assertEqual(new_price, prod_price_change_obj.new_price)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
