from django.conf import settings
from typing import Literal

from shop.models import Product


class Cart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.vendor_code)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity, 'price': str(product.price)}
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def update_quantity(self, product: Product, quantity: int, mode: Literal['plus', 'minus', 'set_value']):
        product_id = str(product.vendor_code)
        if product_id not in self.cart:
            return  
        if mode == 'plus':
            self.cart[product_id]['quantity'] += quantity
        elif mode == 'minus':
            self.cart[product_id]['quantity'] -= quantity
        elif mode == 'set_value':
            self.cart[product_id]['quantity'] = quantity
        self._check_product_quantity(product)
        self.save()

    def _check_product_quantity(self, product):
        product_id = str(product.vendor_code)
        if self.cart[product_id]['quantity'] == 0:
            self.remove(product)

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.vendor_code)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(vendor_code__in=product_ids)
        for product in products:
            self.cart[str(product.vendor_code)]['product'] = product

        for item in self.cart.values():
            item['price'] = int(item['price'])
            item['total_price'] = (item['price'] * item['quantity'])
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        price = sum(int(item['price']) * item['quantity'] for item in self.cart.values())
        return price
            
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
