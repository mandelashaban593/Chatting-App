'''api utilities'''
from django.utils import timezone
from django.utils.dateformat import format
from api.response_codes import API_RESPONSE
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from api.network_extensions import COUNTRY, NETWORK, COUNTRY_CODES





def ApiResponse(responsecode, response=None, exception=None, statuscode=None):
    '''
    control api response
    '''
    description = ''
    try:
        description = API_RESPONSE[responsecode]
    except Exception, e:
        print e
    if not response:
        response = {}
    response['response'] = description
    response['responsecode'] = responsecode
    response['timestamp'] = format(timezone.now(), 'U')
    if exception and settings.DEBUG_API:
        response['exception'] = exception
    if not statuscode:
        statuscode = status.HTTP_200_OK
    return Response(response, status=statuscode)



def validate_number(number):
    '''
    validate a phone number
    requires countrycode
    '''
    valid = False
    responsecode = None
    network_codes = {}
    countrycode = number[:3]
    networkcode = number[3:][:2]
    countrycode = int(countrycode)
    if countrycode in COUNTRY.values():
        countrycode = int(countrycode)
        try:
            network_codes = COUNTRY_CODES[countrycode]
        except Exception, e:
            print e
        responsecode = 13
        for code in network_codes:
            if networkcode in code:
                valid = True
    else:
        responsecode = 12
    return valid, responsecode, countrycode, networkcode
