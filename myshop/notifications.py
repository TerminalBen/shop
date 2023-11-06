import os
from twilio.rest import Client
from celery import shared_task
from myshop.creds import twilio_account_sid,twilio_auth_token
    """This is not in use in the project yet. It will be its own separated app, or centralized project controller to handle all notifications

    """

@shared_task
def sendSMS(to:str) -> int:
    # """Sends sms using the twilio api

    # Args:
    #     to (string): phone number of the recipient
    #     message (string): text to be sent
    # """
    # # Find your Account SID and Auth Token at twilio.com/console
    # # and set the environment variables. See http://twil.io/secure
    try:
        client = Client(twilio_account_sid, twilio_auth_token)

        message = client.messages.create(
                body='Order test',
                from_='+19784876292',
                to=to
            )
        print(message.sid)
    except:
        print("error sending sms")