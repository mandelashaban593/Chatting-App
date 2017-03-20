'''context processors'''
from django.conf import settings


def global_vars(request):
    '''global_vars'''
    data = {
     'BASE_URL': settings.BASE_URL,
     'APP_NAME': settings.APP_NAME,
     #'CUSTOMER_CARE_NUMBER': settings.CUSTOMER_CARE_NUMBER,
     #'CUSTOMER_CARE_EMAIL': settings.CUSTOMER_CARE_EMAIL,
     #'ANALYTICS': settings.ANALYTICS,
     #'LIVE_CHAT': settings.LIVE_CHAT,
     #'PRICING': settings.PRICING,
     #'PRICING_FEATURES': settings.PRICING_FEATURES,
     }
    return data
