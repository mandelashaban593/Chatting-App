'''custom filters'''
from django.template import Library
register = Library()
from django.contrib.humanize.templatetags.humanize import intcomma
from decimal import Decimal
from django.utils.datastructures import SortedDict
from django import forms
from django.forms.forms import NON_FIELD_ERRORS
from django.forms.util import ErrorDict 
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.timesince import timesince
from django.template.defaultfilters import stringfilter
import hashlib

@register.filter
def nice_errors(form, non_field_msg='General form errors'):
    this_nice_errors = ErrorDict()
    if isinstance(form, forms.BaseForm):
        for field, errors in form.errors.items():
            if field == NON_FIELD_ERRORS:
                key = non_field_msg
            else:
                key = form.fields[field].label
            this_nice_errors[key] = errors
    return this_nice_errors


@register.filter
def age(value):
    now = datetime.now(timezone.utc)
    try:
        difference = now - value
    except Exception, e:
    	print e
        return value

    if difference <= timedelta(minutes=1):
        return 'just now'
    return '%(time)s ago' % {'time': timesince(value).split(', ')[0]}


@register.filter
@stringfilter
def trim(value):
    value = value.replace(" ", "")
    return value.strip().lower()


@register.filter(name='md5')
def md5_string(value):
    return hashlib.md5(value).hexdigest()


@register.filter
def multiply(value, arg):
    return value*arg


@register.filter
def payment_discount(whole):
    percent = 20
    discount = (percent * whole) / 100.0
    return int(whole - discount)


@register.filter
def currency(value):
    '''
    extend this to format to default currency
    '''
    dollars = 0
    try:
        #dollars = Decimal(str(value))
        dollars = round(int(value),0)
    except Exception, e:
        pass
    return "%s" % (intcomma(int(dollars)))


@register.filter
def exchange(value):
    '''
    extend this to format to default currency
    '''
    dollars = 0.00
    try:
        dollars = Decimal(str(value))
    except Exception:
        pass
    return "USD %s%s" % (intcomma(int(dollars)), ("%0.2f" % dollars)[-3:])


@register.filter
def filter_response(response):
    '''filter visa and mobile response for display'''
    response = response.replace('{','')
    response = response.replace('}','')
    response = response.replace(', ',' <br /><br />')
    response = response.replace("u'","'")
    response = "<pre>%s</pre>" % response
    return response