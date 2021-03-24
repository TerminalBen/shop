from .cart import Cart
#instantiate the cart using the request object and make it available to other templates as variable names 'cart'
#makes the current car object available to all templates with cart as name
#next setting.py to add context:processors
#than base.html add django template to html
def cart_context(request):
    return {'cart':Cart(request)}