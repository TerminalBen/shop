from django.shortcuts import render
import braintree
from django.shortcuts import render, redirect,get_object_or_404
from django.conf import settings
from orders.models import Order, OrderItem,Product

# Create your views here.

gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

def payment_process(request):

    order_id = request.session.get('order_id')
    order = get_object_or_404(Order,id = order_id)
    orderItems = order.get_items()
    total_cost = order.get_total_cost()
    
    if request.method == 'POST':
        #retireve nonce
        nonce = request.POST.get('payment_method_nonce',None)
        #create and submit transaction
        result = gateway.transaction.sale({
            'amount' : f'{total_cost : .2f}',
            'payment_method_nonce' : nonce,
            'options': {
                'submit_for_settlement':True
            }
        })
        #response_code = result.Transaction.processor_response_code //check these debugs errors
        #response_text = result.Transaction.processor_response_text //check these debug errors
        if result.is_success:
            #Update quantity in DB
            
            for item in orderItems:
                product = get_object_or_404(Product,id=item.product_id)
                product.set_product_stock(OrderItem.get_quantity(item))
                
            #mark the order as paid
            order.paid = True
            #store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payment:done')
        else:
            print(f'result message: {result.message}')
            #print(f'error: {response_code}')
            print(f'error: -------------------')
            # print({f'error message: {response_text}'})
            print({f'error message: ------------------'})
            for error in result.errors.deep_errors:
                print(error.attribute)
                print(error.code)
                print(error.message)
            return redirect('payment:canceled')
    else:
        #generate token
        client_token = gateway.client_token.generate()
        return render(request,'payment/process.html',{'order':order,'client_token':client_token})

def payment_done(request):
    return render(request, 'payment/done.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')
