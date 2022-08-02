from celery import task
from io import BytesIO
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order

@task
def payment_completed_user(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    # create invoice e-mail
    subject = f'My Shop - EE Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject,message,'admin@myshop.com',[order.email])
    # generate PDF
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out,
    stylesheets=stylesheets)
    # attach PDF file
    email.attach(f'order_{order.id}.pdf',out.getvalue(),'application/pdf')
    # send e-mail
    email.send()


@task
def payment_completed_admin(order_id):
    """
    Task to send an e-mail notification to admin when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    # create invoice e-mail
    subject = f'Admin Invoice - EE Invoice no. {order.id}'
    message = f'Please, find attached the invoice for the most recent(order number {order.id}) purchase.'
    email = EmailMessage(subject,message,'admin@myshop.com',["bentolima100@gmail.com"])
    # generate PDF
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out,
    stylesheets=stylesheets)
    # attach PDF file
    email.attach(f'order_{order.id}.pdf',out.getvalue(),'application/pdf')
    # send e-mail
    email.send()