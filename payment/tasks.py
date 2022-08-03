from celery import task
from io import BytesIO
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order
from twilio.rest import Client
from myshop.creds import twilio_account_sid,twilio_auth_token


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


@task
def send_sms_on_payment(to,order_id,name):
    """Sends sms using the twilio api

    Args:
        to (string): phone number of the recipient
        message (string): text to be sent
    """
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure

    # account_sid = os.environ['TWILIO_ACCOUNT_SID']
    # auth_token = os.environ['TWILIO_AUTH_TOKEN']

    client = Client(twilio_account_sid, twilio_auth_token)

    message = client.messages.create(
            body=f'Dear {name},\n Your Payment for the order number {order_id} has been received, and we are already processing the order. \n Please check your email for the receipt. \n The Store.',
            from_='+19784876292',
            to=to
        )

    print(message.sid)