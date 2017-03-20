'''accounts models'''
from django.db import models
# Create your models here.
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.conf import settings
import urllib
import hashlib
from rest_framework.authtoken.models import Token
from registration.signals import user_registered, user_activated
from django.contrib.auth import login
from django.core.validators import RegexValidator
from django.contrib.admin.models import LogEntry
from remitapi.utils import COUNTRY_CHOICES, NETWORK_CHOICES


class Company(models.Model):
    '''user profiles'''
    owner = models.OneToOneField(User)
    name = models.CharField(blank=True, max_length=250)
    is_verified = models.BooleanField(default=False)


class UserProfile(models.Model):
    '''user profiles'''
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='profile')
    firstname = models.CharField(blank=True, max_length=50)
    lastname = models.CharField(blank=True, max_length=50)
    phone_regex = RegexValidator(
        regex = r'^\+?1?\d{9,15}$',
        message = "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )
    phonenumber = models.CharField(validators=[phone_regex], blank=True, max_length=20)


    @property
    def avatar(self, size="100"):
        '''gravatar image'''
        gravatar_url = settings.GRAVATAR_URL
        gravatar_url += urllib.urlencode({
            'gravatar_id': hashlib.md5(self.user.email).hexdigest(),
            'size': str(size)
        })
        return gravatar_url

    @property
    def names(self):
        name = u"%s" % self.user.email
        if self.firstname:
            name = u"%s %s" % (
                self.firstname,
                self.lastname
                )
        return name


def initial_messages(user, request):
    print "send initial messages"


def user_registered_callback(sender, user, request, **kwargs):

    '''save profile and create company'''
    #data = request.POST
    profile = UserProfile(user=user)
    profile.save()
    Token.objects.create(user=user)
    try:
        '''company'''
        company = Company(user=user)
        company.save()
    except Exception, e:
        print e

    try:
        initial_messages(user, request)
    except Exception, e:
        print e

    '''login user after registration'''
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)


def login_on_activation(sender, user, request, **kwargs):
    """Logs in the user after activation"""
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)


user_registered.connect(user_registered_callback)
user_activated.connect(login_on_activation)



class LoginInfo(models.Model):
    '''store login data'''
    login_time = models.DateTimeField(auto_now_add=True)
    user_agent = models.CharField(max_length=1000, blank=True, null=True)
    remote_addr = models.GenericIPAddressField()
    user = models.ForeignKey(User, blank=False, null=False)


class UserActions(models.Model):
    '''store user actions'''
    session = models.ForeignKey(LoginInfo, blank=False, null=False)
    log_entry = models.ForeignKey(LogEntry, blank=False, null=False)
    user = models.ForeignKey(User, blank=False, null=False)


    @property
    def user_location(self):
        location = 'UnKnown'
        try:
            if self.session.remote_addr:
                import requests
                r = requests.get('http://ipinfo.io/%s/json' % self.session.remote_addr)
                loc = r.json()
                if 'ip' in loc:
                    location = '%s' % loc['ip']
                if 'country' in loc:
                    location += ',%s' % loc['country']
                if 'city' in loc:
                    location += ',%s' % loc['city']
                if 'region' in loc:
                    location += ',%s' % loc['region']
        except Exception, e:
            pass
        return location


class AdminProfile(models.Model):


    class Meta:
        permissions = (
            ('view_audit_trail', 'View Audit Trails'),
        )

    '''profile for the admin user'''
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='admin_profile')
    country = models.CharField(
        blank=True, max_length=100, choices=COUNTRY_CHOICES, default=False)

    mobile_network = models.CharField(
        blank=True, max_length=100, choices=NETWORK_CHOICES, default=False)

    is_customer_care = models.BooleanField(default=False)

    @property
    def uid(self):
        '''return user'''
        return str(self.pk ^ 0xABCDEFAB)

    @property
    def permissions(self):
        '''get a stuff users permissions'''
        user_permissions = {}
        for x in Permission.objects.filter(user=self.user):
            user_permissions.update({x.codename: True})
        return user_permissions

    @property
    def avatar(self, size="100"):
        '''gravatar image'''
        gravatar_url = settings.GRAVATAR_URL
        gravatar_url += urllib.urlencode({
            'gravatar_id': hashlib.md5(self.user.email).hexdigest(),
            'size': str(size)
        })
        return gravatar_url
