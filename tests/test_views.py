from django.test import TestCase
from shop.models import Seller, Product, Sale

class ProductsListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        seller = Seller.objects.create(name='Mike')
        product = Product.objects.create(title='Product title 1', description='Product description 1', price=34.99, quantity=20, seller=seller)
        Sale.objects.create(seller=seller, product=product, quantity_sold=10)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)