from django.conf.urls import url
from .views import ProductList

urlpatterns = [
    url('', ProductList.as_view(), name='product_list'),
]