# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir)) + '/'

SSLIFY_DISABLE = True
DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEBUG_PAYMENTS = DEBUG


MTN_SDP_USERNAME = ''
MTN_SDP_PASS = ''
MTN_SDP_SERVICEID = ''
MTN_SDP = ''
MTN_SDP_URL = ''
MTN_VENDOR_CODE = ''


DEBUG_API = True

ADMINS = (
    ('Madra David', 'madra@redcore.co.ug'),
)


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR + 'run', 'dev.db'),
    }
}

#BASE_URL = 'http://127.0.0.1/pesapot/'
BASE_URL = 'http://127.0.0.1:8000/'


ANONYMOUS_USER_ID = 1

#PEGPAY

PEGPAY_URL = ''
PEGPAY_USERNAME=""
PEGPAY_PASSWORD=""
PEGPAY_CHEQUE_NUMBER=""
PEGPAY_PAYMENT_TYPE=''

LIVE = 0
DISABLE_COMMS = True

#celery
BROKER_URL = "amqp://"

#remitussd
USSDREMIT_KEY = ''
USSDREMIT_TOKEN = ''
USSDREMIT_TRANSACTIONSTATUS_URL = ''

USEREMIT_KEY = ''
USEREMIT_TOKEN = ''
USEREMIT_TRANSACTIONSTATUS_URL = ''

AFRICAT_USERNAME = ""
AFRICAT_KEY = ""


RWANDA_USERNAME = ''
RWANDA_PASSWORD = ''
RWANDA_URL = ''
RWANDA_AUTHKEY = ''
RWANDA_SECRET = ''



Beyonic_URL = ""
Beyonic_Call_URL = ""
Beyonic_Callback_URL = ""




IMPAL_USERNAME = ""

IPAY_KEY = ""
IPAY_VENDOR = ""
IPAY_MM_URL = ""
IPAY_TS_URL = ""

VIT_URL = ""
SSLIFY_DISABLE = True