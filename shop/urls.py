from django.urls import path
from .views import ProductList, ProductDetail, SalesList

urlpatterns = [
    path('product_detail/<int:product_id>/', ProductDetail.as_view(), name='product_detail'),
    path('sales_list/', SalesList.as_view(), name='sales_list'),
    path('', ProductList.as_view(), name='product_list'),
]