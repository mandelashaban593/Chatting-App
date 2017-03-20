import remitapi.settings as settings
from django.template.loader import render_to_string
import requests


def clean_phonenumber(number):
    try:
        number = number.replace('-', '')
        number = number.replace(' ', '')
        number = number.replace(',', '')
    except Exception, e:
        debug(e, 'Error cleaning phonenumber %s' % number, 'sms')
    return number


def debug(error, message='', efile=''):
    from remitapi.utils import debug
    return debug(error, message, efile)


def nexmo_sms(to, message):
    from nexmo.libpynexmo.nexmomessage import NexmoMessage
    title = settings.NEXMO_FROM

    to = clean_phonenumber(to)

    try:
        if to[0] == 1:
            title = '12134657620'
    except Exception, e:
        debug(e, 'send sms error', 'sms')

    params = {
        'api_key': settings.NEXMO_USERNAME,
        'api_secret': settings.NEXMO_PASSWORD,
        'from': title,
        'to': '%s%s' % ('+', to),
        'text': message,
    }
    # print params
    sms = NexmoMessage(params)
    response = sms.send_request()
    return response


def twilio_sms(to, message):
    from twilio.rest import TwilioRestClient
    response = False
    to = clean_phonenumber(to)
    try:
        if not to[0] == '+':
            to = '%s%s' % ('+', to)
    except Exception, e:
        debug(e, 'Error sending twilio sms', 'sms')

    client = TwilioRestClient(
        settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    response = client.messages.create(
        body=message, to=to, from_='+16092574786')
    try:
        debug(e, 'Twilio sms response %s' % response, 'sms')
    except Exception, e:
        debug(e, 'Twilio sms response %s' % response, 'sms')
    return response

def sukuma_sms(to, message):

    data = {
        'sender': settings.SUKUMA_SENDER,
        'contacts': to,
        'message': message,
        'username': settings.SUKUMA_USERNAME,
        'password': settings.SUKUMA_PASSWORD
    }
    response = None

    try:
        response = requests.post(settings.SUKUMA_ENDPOINT, params=data)
        print ':sukuma sms success ',str(response.content)
    except Exception as e:
        print ':Sukuma sms failure ',str(e)
        debug(e, 'Sukuma sms response %s' % response.content, 'sms')
    return response

def africatalking_sms(to,message):
    """africa is talking sms."""
    from africatalking_gateway import AfricasTalkingGateway, AfricasTalkingGatewayException

    username = settings.AFRICAT_USERNAME
    apikey = settings.AFRICAT_KEY
    response = None

    try:
        gateway = AfricasTalkingGateway(username, apikey)

        response = gateway.sendMessage(to, message)

        print ':Africa Response success ',str(response)
    except AfricasTalkingGatewayException, e:
        response = 'africa sms error: %s' % str(e)
        print ':Africa sms fail ',str(e)

    return response
