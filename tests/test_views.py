from django.test import TestCase
from django.shortcuts import reverse

class ProductsListViewTest(TestCase):
    fixtures = ['fixtures/seller.json', 'fixtures/product.json', 'fixtures/sale.json']

    def test_product_exists_on_page(self):
        resp = self.client.get(reverse('product_list'))
        self.assertTrue('Product title 1' in [el['title'] for el in resp.context['products'].values()])