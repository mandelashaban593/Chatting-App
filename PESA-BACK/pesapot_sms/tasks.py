from celery.task.schedules import crontab
from celery.decorators import periodic_task, task
from celery.utils.log import get_task_logger
from sms import *
from django.conf import settings
logger = get_task_logger(__name__)


@task(name="pesapot_sms")
def send_pesapot_sms(to, sms_client, sms_message, sms_agent):
    """
    send client sms.
    sms_agent:
    1.nexmo
    2.twilio
    3.sukuma
    """


    response = False

    if sms_agent == 1:
        response = nexmo_sms(to, sms_message)
    elif sms_agent == 2:
        response = twilio_sms(to, sms_message)
    elif sms_agent == 3:
        response = sukuma_sms(to, sms_message)
    elif sms_agent == 4:
        response = africatalking_sms(to, sms_message)
    
    logger.info("Sent pesapot sms: ")
