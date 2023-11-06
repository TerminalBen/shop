#from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
#from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods

from shop.models import Product
from .cart import Cart
from .forms import cart_add_form
from coupons.forms import CouponApplyForm

#@require_POST()
@require_http_methods(["POST"])
def cart_add(request,product_id):
    cart=Cart(request)
    product = get_object_or_404(Product,id=product_id)
    form=cart_add_form(request.POST)
    if form.is_valid():
        cd=form.cleaned_data
        cart.add(product=product,quantity=cd['quantity'],override_quantity=cd['override'])
    return redirect('cart:cart_detail')

#@require_POST()
@require_http_methods(["POST"])
def cart_remove(request,product_id):
    cart=Cart(request)
    product= get_object_or_404(Product,id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart=Cart(request)
    for item in cart:
        item['update_quantity_form'] = cart_add_form(initial={'quantity':item['quantity'], 'override':'True'})
    coupon_apply_form = CouponApplyForm()
    return render(request,'cart/detail.html',{'cart':cart,'coupon_apply_form':coupon_apply_form})

#def cart_in_frontpage(request):
#    return render(request,'shop/base.html',{'cart':cart.})




