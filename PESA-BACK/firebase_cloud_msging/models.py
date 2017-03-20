from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class NotifsClient(models.Model):
    """Notification client."""
    client_name = models.CharField(blank=False, max_length=100,unique=True)
    api_key = models.CharField(blank=False, max_length=300, unique=True)
    added = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)
    #user = models.ForeignKey(User, unique=True)
    user = models.ForeignKey(User)

    @property
    def client_id(self):
        '''Client id.'''
        return str(self.pk ^ 0xABCDEFAB)
