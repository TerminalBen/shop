from django.http import HttpResponse
from django.shortcuts import render,redirect
from django .conf import settings
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created_admin, order_created_user
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from .models import Order
from django.template.loader import render_to_string
import os


from weasyprint import HTML,CSS

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
            #launch asynchronous tasks
            order_created_user(order.id)
            order_created_admin(order.id)
            #sendSMS("+2385841700")
            
            #set the order in the session
            request.session['order_id'] = order.id
            #redirect to payment
            return redirect(reverse('payment:process'))
    else:
        form=OrderCreateForm()
    return render(request,'orders/order/create.html',{'cart':cart,'form':form})

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order,id=order_id)
    return render(request,'admin/orders/order/detail.html',{'order': order})

@user_passes_test(lambda u:u.is_staff)
def admin_order_pdf(request,order_id):
    order = get_object_or_404(Order,id = order_id)
    html = render_to_string('orders/order/pdf.html',{'order':order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    HTML(string=html).write_pdf(response,
    stylesheets=[CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    return response


