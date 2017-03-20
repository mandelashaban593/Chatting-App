'''remit api tool views'''
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404,\
    HttpResponse
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from remitapi.decorators import login_required
from accounts.models import UserProfile
from remitapi.models import ApiTransaction, Wallet
from django.db.models import Q
from mtn.models import MtnTransaction
from pegpay.models import UtilityTransaction


@login_required
def render_view(request, template, data):
    '''
    wrapper for rendering views , loads RequestContext
    @request  request object
    @template  string
    @data  tumple
    '''
    template = 'dashboard/%s' % template
    data['STATIC_URL'] = '%sdashboard/' % settings.STATIC_URL
    if request.user.is_authenticated():
        data['profile'] = UserProfile.objects.get(user=request.user)
    return render_to_response(
        template, data,
        context_instance=RequestContext(request)
    )


def home(request):
    '''
    dashboard page
    '''
    transactions = ApiTransaction.objects.filter(
        user=request.user.pk
        ).order_by('-id')
    usd_wallet = Wallet.objects.filter(
        user=request.user.pk,
        currency='USD'
        )
    ugx_wallet = Wallet.objects.filter(
        user=request.user.pk,
        currency='UGX'
        )
    kes_wallet = Wallet.objects.filter(
        user=request.user.pk,
        currency='KES'
        )

    usd_balance = ugx_balance = kes_balance = 0.0
    try:
        usd_balance = usd_wallet[0].current_bance
    except Exception:
        pass
    try:
        kes_balance = kes_wallet[0].current_bance
    except Exception:
        pass
    try:
        ugx_balance = ugx_wallet[0].current_bance
    except Exception:
        pass

    return render_view(
        request,
        'index.html', {
        'transactions': transactions,
        'usd_wallet': usd_wallet,
        'ugx': ugx_wallet,
        'kes': kes_wallet,
        'usd_balance': usd_balance,
        'ugx_balance': ugx_balance,
        'kes_balance': kes_balance
        }
    )


def mobilemoney(request):
    '''
    mobile money transactions
    '''
    transactions = ApiTransaction.objects.filter(
        Q(app=MtnTransaction.objects.filter(owner=request.user.pk)),
            )
    return render_view(
        request,
        'mobilemoney.html', {'transactions': transactions}
    )

def billreports(request):
    '''
    Bill payments transactions
    '''
    #transactions={}
    transactions = ApiTransaction.objects.filter(
        Q(app=UtilityTransaction.objects.all()),
            )


    #UtilityTransaction

    print 'bill transactions: ',str(transactions)

    return render_view(
        request,
        'billpaymentreport.html',{'transactions':transactions}
    )




def api_keys(request):
    keys = {}
    return render_view(request, 'api_keys.html',
                       {'keys': keys}
                       )
