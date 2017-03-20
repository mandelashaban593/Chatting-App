from celery.task.schedules import crontab
from celery.decorators import periodic_task, task
from celery.utils.log import get_task_logger

from firebase_cloud_msging.server import FirebaseCloudMessaging

logger = get_task_logger(__name__)

@task(name="push_notification")
def send_push_notification(data):
    """send push notifications."""
    print ':Inside push notification'
    fcm = FirebaseCloudMessaging()
    status = fcm.single_device(**data)
    logger.info(":Sent push notification: "+str(status))
