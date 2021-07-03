from shop.models import Product
from datetime import datetime

def page_gen_datetime(request):
    return {"page_gen_datetime": datetime.now()}
