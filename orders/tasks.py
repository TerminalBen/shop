#from __future__ import absolute_import
from celery import task
from django.core.mail import send_mail
from .models import Order

@task
def order_created_admin(order_id):
    """task to send an email to the shop admins when the order has been created

    Args:
        order_id (integer): id of the order

    Returns:
        integer: send_mail from django.core.mail
    """
    order = Order.objects.get(id=order_id)
    subject = f'order {order.id} from awesomeshop'
    message = f'A new order has been submited \n'f'The order ID is {order.id}.'
    mail_sent = send_mail(subject,message,'admin@shop.com',["bentolima100@gmail.com"])
    return mail_sent

@task
def order_created_user(order_id):
    #task to send an email to the user when the order has been created
    order = Order.objects.get(id=order_id)
    subject = f'order {order.id} from awesomeshop'
    message = f'Dear {order.first_name},\n\n'f'You have successfully placed an order. \n'f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject,message,'admin@shop.com',[order.email])
    return mail_sent

@task
def order_created_user_sms(order_id):
    pass
