from rest_framework.views import exception_handler
from django.shortcuts import HttpResponse
import json


def api_exception_handler(exception, context):
    error = exception_handler(exception, context)
    response = HttpResponse(
        json.dumps({'error': error, 'context': str(context)}),
        content_type="application/json", status=500
    )
    return response
