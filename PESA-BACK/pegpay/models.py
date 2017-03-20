'''Pegpay App'''
from remitapi.models import App
from django.db import models


class UtilityTransaction(App):
    '''Api transactions'''
    referencenum = models.CharField(blank=True, max_length=130)

    account_name = models.CharField(blank=True, max_length=130)
    billtype = models.CharField(blank=True, max_length=130)

    paid_by = models.CharField(blank=True, max_length=130)

    paymethod = models.CharField(blank=True, max_length=130)

    recipient_phone = models.CharField(blank=True, max_length=130)

    sender_message = models.CharField(blank=True, max_length=130)

    vendor_id = models.CharField(blank=True, max_length=130)

    bill_message = models.CharField(blank=True,max_length=50)

    mobile_response_metadata = models.TextField(blank=True, default=False)
    
    beyon_transid = models.CharField(blank=True, max_length=130)

    beyon_sender = models.CharField(blank=True, max_length=130)

    beyon_sender =  models.CharField(blank=True,max_length=50)



    #save request as json


class WaterTransaction(App):
    '''water transactions'''
    customer_ref = models.CharField(blank=False, max_length=130)
    company_code = models.CharField(blank=False, max_length=130)
    transaction_ref = models.CharField(blank=False, max_length=130)
    customer_name = models.CharField(blank=False, max_length=130)
    paid_by = models.CharField(blank=False, max_length=130)
    customer_phone = models.CharField(blank=False, max_length=130)
    sender_message = models.CharField(blank=True, max_length=130)
    area = models.CharField(blank=False, max_length=130)

    """
    def save(self, *args, **kwargs):
        super(WaterTransaction, self).save(*args, **kwargs)
    """


class ElectricityTransaction(App):
    '''Electricity transactions'''
    customer_type = models.CharField(blank=False, max_length=130)
    payment_type = models.CharField(blank=False, max_length=130)
    sender_message = models.CharField(blank=True, max_length=130)
    customer_ref = models.CharField(blank=False, max_length=50)
    customer_name = models.CharField(blank=False, max_length=50)
    customer_phone = models.CharField(blank=False, max_length=50)
    paid_by = models.CharField(blank=False, max_length=50)
    customer_email = models.EmailField(blank = True)
    company_code = models.CharField(blank=False, max_length=50)


    """
    def save(self, *args, **kwargs):
        super(ElectricityTransaction, self).save(*args, **kwargs)
    """
