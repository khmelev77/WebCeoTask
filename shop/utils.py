from .models import Product, Seller

def check_product_exist(product_id):
    try:
        product = Product.objects.filter(pk=product_id)[0]
        return product
    except IndexError:
        return None


def check_seller_exist(product):
    sellers_qs = Seller.objects.filter(product=product.pk)
    if sellers_qs: return sellers_qs
    return None