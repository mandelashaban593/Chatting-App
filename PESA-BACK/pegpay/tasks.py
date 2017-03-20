from celery.task.schedules import crontab
from celery.decorators import periodic_task, task
from celery.utils.log import get_task_logger

from pegpay.server import PegPay
from remit_ussd.remit_ussd import RemitUssd

#from pegpay import track_transaction_status
#from PegPay import track_transaction_status


logger = get_task_logger(__name__)

@task(name="transaction_status")
def check_transaction_status(vendorid, vendor=None, sender_id=None):
    """
    check transaction status,save result to db.
    """
    print ':Task vendor id: ',str(vendorid)
    logger.info(vendorid)
    pegpay = PegPay()
    pegpay.track_transaction_status(vendorid, vendor, sender_id)
    logger.info("Checked transaction status.")
