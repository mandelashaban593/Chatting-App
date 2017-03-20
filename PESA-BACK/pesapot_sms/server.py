import remitapi.settings as settings
import requests
from tasks import send_pesapot_sms


class Sms():
    """handle sms."""

    def __init__(self):
        #nexmo
        print ':Inside Sms'
    def send_sms(self, to, sms_message, sms_client, sms_agent=None):
        """
        sms_agent:
        1=nexmo
        2=twilio
        3=sukuma
        5=africa_talking
        """
        print ':inside send_sms'
        agent = False

        try:
            agent = int(sms_agent)
            #client = int(sms_client)
            print ':String to int success'
        except Exception as e:
            print ':String to int failed: ',str(e)

        send_pesapot_sms.apply_async(countdown=50,kwargs={
            'to': to,
            'sms_client': sms_client,
            'sms_message': sms_message,
            'sms_agent': agent
        })
