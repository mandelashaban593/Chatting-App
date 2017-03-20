'''remit api docs views'''
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404,\
    HttpResponse
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from remitapi.decorators import login_required
from accounts.models import UserProfile
from remitapi.models import ApiTransaction
from django.db.models import Q


def render_view(request, template, data):
    '''
    wrapper for rendering views , loads RequestContext
    @request  request object
    @template  string
    @data  tumple
    '''
    template = 'docs/%s' % template
    data['STATIC_URL'] = '%sdocs/' % settings.STATIC_URL
    return render_to_response(
        template, data,
        context_instance=RequestContext(request)
    )


def home(request):
    '''
    landing page
    '''
    return render_view(
        request,
        'index.html', {}
    )


def apidocs(request):
    '''
    landing page
    '''
    return render_view(
        request,
        'apidocs.html', {}
    )
