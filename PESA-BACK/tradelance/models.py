from remitapi.models import App
from django.db import models

# Create your models here.
class TlanceTransaction(App):
    api = models.CharField(blank=True,max_length=130)
