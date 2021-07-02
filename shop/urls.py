from django.urls import path
from .views import ProductList, ProductDetail

urlpatterns = [
    path('product_detail/<int:product_id>/', ProductDetail.as_view(), name='product_detail'),
    path('', ProductList.as_view(), name='product_list'),
]