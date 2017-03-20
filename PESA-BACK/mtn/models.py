'''Mtn App models'''
from remitapi.models import App
from django.db import models
from jsonfield import JSONField


class MtnTransaction(App):
    '''Api transactions'''
    response = JSONField()
    phonenumber = models.CharField(max_length=20)
