'''background tasks'''
from django.core.mail import EmailMultiAlternatives
from background_task import background
from django.conf import settings
from django.template.loader import render_to_string



# @task(name="pesapot_sms")
# def send_pesapot_sms(to,):



@background(schedule=20)
def send_email(subject, text_content, sender, receipient, html_content):
    '''schedule email sending'''
    msg = EmailMultiAlternatives(subject, text_content, sender, [receipient])
    msg.attach_alternative(html_content,  "text/html")
    msg.send()
    print "Mail sent to %s from %s" % (receipient, sender)


@background(schedule=20)
def send_sms(to, template, content, message=False):
	from i99fix.utils import debug
	from twilio.rest import TwilioRestClient

	if settings.DISABLE_COMMS:
		return True

	content.update({
	'BASE_URL': settings.BASE_URL,
	'APP_NAME': settings.APP_NAME
	})
	if not message:
		message = render_to_string(template, content)
		message = message.encode('utf-8')

	response = False
	try:
	    if not to[0] == '+':
	        to ='%s%s' % ('+', to)
	except Exception, e:
		print e
	client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
	response = client.messages.create(body=message, to=to, from_='+14049943695')
	try:
	    debug(e,'Twilio sms response %s' % response,'sms')
	except Exception, e:
	    pass
	return response
