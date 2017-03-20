'''Api models'''
from django.db import models
from jsonfield import JSONField


class PaybillAccount(models.Model):
    '''Api transactions'''
    details = JSONField(blank=True)
    referencenumber = models.CharField(max_length=100)
    location = models.CharField(max_length=100, default='')
    billtype = models.IntegerField(blank=False, default=1)
    vendorid = models.CharField(max_length=100, default='')
    send_date = models.CharField(max_length=100, default='')
    modified_date = models.DateTimeField(auto_now=True)

    def updatedetails(self):
   		print "updating data"
