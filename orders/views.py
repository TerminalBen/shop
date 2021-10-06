from django.shortcuts import render,redirect
#from .models import Order
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created_user
from django.urls import reverse
# Create your views here.

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order=form.save()
            for item in cart:
                OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'])
            cart.clear()
            #launch asynchronous task
            order_created_user.delay(order.id)

            # TODO start another asynchronout task for the shop admins
            # TODO order_created_admins(order_id)
            # TODO:fix bug where item order doesnt appear in created template (FIXED)
            #return render(request,'orders/order/created.html',{'order':order})
            #set the order in the session
            request.session['order_id'] = order.id
            #redrect to payment
            return redirect(reverse('payment:process'))
    else:
        form=OrderCreateForm()
    return render(request,'orders/order/create.html',{'cart':cart,'form':form})


