'''Mtn App models'''
from remitapi.models import App
from django.db import models
from jsonfield import JSONField


class IpayTransaction(App):
    '''Api transactions'''
    response = JSONField()
    phonenumber = models.CharField(max_length=20)
    txnref = models.CharField(max_length=50)
    recipient = models.CharField(max_length=250)
    mnoreceipt = models.CharField(max_length=150)
    credit = models.DecimalField(blank=True,
    	null=True, decimal_places=2, max_digits=10)
    txncost = models.DecimalField(
        default=0.0, decimal_places=2, max_digits=10)
