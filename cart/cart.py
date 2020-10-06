from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart(object):
    '''
    initialize cart
    '''
    def __init__(self,request):
        self.session=request.session
        cart= self.session.get(settings.CART_SESSION_ID)

        if not cart:
            #save an empty cart in session
            cart= self.session[settings.CART_SESSION_ID] = {}
        sef.cart= cart

    def add(self, product,quantity=1, override_quantity = False):
        '''
            Add an item to the cart and update the quantity
        '''

        product_id=str(product.id)
        if product_id not in self.cart:
            self.cart[product_id]= {'quantity':0,'price':str(product.price)}
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self,product):
        product_id=str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def __iter__(self):
        '''
        iterate over the items in the cart to get real values from the DB
        '''
        product_ids=self.cart.keys()
        #get the product object and add them to the cart
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * Decimal(item['quantity'])
            yield item

    def __len__(self):
        qt=0
        for item in self.cart.values()
            qt += item['quantity']