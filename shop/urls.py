from django.urls import path
from .views import ProductList, ProductDetail, SalesList, PriceChangelog

urlpatterns = [
    path('product_detail/<int:product_id>/', ProductDetail.as_view(), name='product_detail'),
    path('sales_list/', SalesList.as_view(), name='sales_list'),
    path('price_changelog/<int:product_id>/', PriceChangelog.as_view(), name='price_changelog'),
    path('', ProductList.as_view(), name='product_list'),
]