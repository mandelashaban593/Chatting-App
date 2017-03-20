'''api views'''
from ipay.serializers import DepositMoneySerializer
from ipay.server import Ipay
from api.utils import ApiResponse
from api.views import ApiView
from ipay.models import IpayTransaction
from remitapi.models import KESWallet
import json
from remitapi.utils import balance_low_email


def balance(user):
    balance = 0
    try:
        wallet = KESWallet.objects.get(user=user)
        balance = wallet.current_balance
        print balance
    except Exception, e:
        pass
    return balance


def msisdn_valid(msisdn, network):
    valid = False
    try:
        if msisdn[:3] == '254':
            valid = True
    except Exception, e:
        pass
    return valid


class DepositMoney(ApiView):

    """
    DepositMoney for Mtn number
    """
    serializer_class = DepositMoneySerializer
    queryset = {}
    network = None

    def post(self, request):
        '''check if a number is registered'''
        response = {}
        responsecode = 0
        transactionid = None
        exception = None
        '''
        get the transactionid
        '''
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            msisdn = serializer.validated_data['phonenumber']
            if not msisdn_valid(msisdn, self.network):
                responsecode = 6
            elif float(balance(request.user)) < float(amount):
                responsecode = 11
                response['detail'] = "You need a minimum of KES %s on your KESWallet to perform this transaction" % amount
            else:
                responsecode, response, exception = IpayDepositMoney(msisdn, amount, request.user)
        else:
            responsecode = 7
            response['errors'] = serializer.errors
        return ApiResponse(
            responsecode, response, exception
            )


def IpayDepositMoney(msisdn, amount, user):
    response = {}
    exception = None
    responsecode = 10
    ipay = Ipay()
    try:
        transaction = IpayTransaction(
            amount=amount,
            owner=user,
            phonenumber=msisdn
        )
        transaction.save()
        transactionid = transaction.transactionid
    except Exception, e:
        exception = e
    if transactionid:
        result = ipay.DepositMoney(transaction)
        status = 0
        txnref = ''
        mnoreceipt = ''
        recipient = ''
        txncost = None
        credit = None
        try:
            result = result.replace('}{', ',')
            result = json.loads(result)
            status = result.get('status', 0)
            status = int(status)
            txnref = result.get('txnref', '')
            mnoreceipt = result.get('mnoreceipt', '')
            recipient = result.get('msisdn_name', '')
            txncost = result.get('txncost', None)
            credit = result.get('credit', None)
        except Exception, e:
            print e
        if 'error' in result:
            if not status == 1:
                responsecode = 10
            exception = result
        if status == 1 and txncost and credit:
            responsecode = 4
            try:
                transaction.txncost = float(txncost)
                transaction.credit = float(credit)
                transaction.save()
            except Exception, e:
                pass
            try:
                '''if transaction successful deduct from sender'''
                wallet = KESWallet(
                    user=user,
                    debit=amount
                    )
                wallet.save()
            except Exception, e:
                pass
        #if status == '2' or status == 2:
        #    responsecode = 10
        #    balance_low_email(request, 'KES', transaction)
        response['transactionid'] = transactionid
        transaction.response = result
        transaction.txnref = txnref
        transaction.mnoreceipt = mnoreceipt
        transaction.recipient = recipient
        transaction.save()
    return responsecode, response, exception
