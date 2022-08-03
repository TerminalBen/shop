import os
from twilio.rest import Client
from celery import task
from myshop.creds import twilio_account_sid,twilio_auth_token

@task
def sendSMS(to):
    # """Sends sms using the twilio api

    # Args:
    #     to (string): phone number of the recipient
    #     message (string): text to be sent
    # """
    # # Find your Account SID and Auth Token at twilio.com/console
    # # and set the environment variables. See http://twil.io/secure

    # # account_sid = os.environ['TWILIO_ACCOUNT_SID']
    # # auth_token = os.environ['TWILIO_AUTH_TOKEN']

    # client = Client(twilio_account_sid, twilio_auth_token)

    # message = client.messages.create(
    #         body='Order test',
    #         from_='+19784876292',
    #         to=to
    #     )

    # print(message.sid)
    pass