from django.shortcuts import render,redirect
#from .models import Order
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created_user
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order
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
            
            #set the order in the session
            request.session['order_id'] = order.id
            #redrect to payment
            return redirect(reverse('payment:process'))
    else:
        form=OrderCreateForm()
    return render(request,'orders/order/create.html',{'cart':cart,'form':form})

@staff_member_required
def admin_order_details(request, order_id):
    order = get_object_or_404(Order,id=order_id)
    return render(request,'admin/orders/order/detail.html',{'order',order})


