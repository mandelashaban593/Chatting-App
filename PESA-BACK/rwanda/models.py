'''Mtn App models'''
from remitapi.models import App
from django.db import models
from jsonfield import JSONField


class RwandaTransaction(App):
    '''Api transactions'''
    response = JSONField()
    phonenumber = models.CharField(max_length=20)
    txnref = models.CharField(max_length=50, blank=True, null=True)
    senderreason = models.CharField(max_length=50, default="From Remit")
    sendername = models.CharField(max_length=50, default="Remit")
    credit = models.DecimalField(blank=True,
                                 null=True, decimal_places=2, max_digits=10)
    txncost = models.DecimalField(
        default=0.0, decimal_places=2, max_digits=10)
