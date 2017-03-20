'''api views'''
from rwanda.serializers import DepositMoneySerializer
from rwanda.server import Rwanda
from api.utils import ApiResponse
from api.views import ApiView
from rwanda.models import RwandaTransaction
from remitapi.models import RWFWallet
from remitapi.utils import debug as udebug
from remitapi.utils import insufficient_account_balance


def debug(error, message):
    return udebug(error, message, 'rwanda')


def balance(user):
    balance = 0
    try:
        wallet = RWFWallet.objects.get(user=user)
        balance = wallet.current_balance
    except Exception, e:
        debug(e, 'check rwanda blance')
    return balance


def msisdn_valid(msisdn, network):
    valid = False
    try:
        if msisdn[:3] == '250':
            valid = True
    except Exception, e:
        debug(e, 'format rwanda blance')
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
                response[
                    'detail'] = "You need a minimum of RWF %s on \
                    your RWFWallet to perform this transaction" % amount
            else:
                responsecode, response, exception = RwandaDepositMoney(
                    msisdn, amount, request.user)
        else:
            responsecode = 7
            response['errors'] = serializer.errors
        return ApiResponse(
            responsecode, response, exception
        )


def RwandaDepositMoney(msisdn, amount, user):
    '''
    DepositMoney Api view
    '''
    response = {}
    exception = None
    transactionid = None
    referenceid = ''
    responsecode = 10
    status = 0
    rwanda = Rwanda()
    try:
        transaction = RwandaTransaction(
            amount=amount,
            owner=user,
            phonenumber=msisdn
        )
        transaction.save()
        transactionid = transaction.transactionid
    except Exception, e:
        exception = e
    if transactionid:
        result = rwanda.DepositMoney(transaction)

        """
        import sys
        old_stdout = sys.stdout
        log_file = open("/media/data/sites/remitapi/rwanda.log", "a")
        sys.stdout = log_file
        print result
        sys.stdout = old_stdout
        log_file.close()
        print result
        """

        try:
            import json
            result = json.loads(result)
            status = result.get('success', status)
            responsecode = result.get('responsecode', responsecode)
            responsecode = int(responsecode)
            referenceid = result.get('referenceid', None)
        except Exception, e:
            debug(e, 'rwanda response error')
        print status
        print responsecode
        if responsecode == 2001:
            responsecode = 0
            try:
                wallet = RWFWallet(
                    user=user,
                    debit=amount
                )
                wallet.save()
            except Exception, e:
                pass
        else:
            if responsecode == 1104:
                responsecode = 16
            else:
                if responsecode == 1108:
                    insufficient_account_balance(transaction)
                responsecode = 9
        response['transactionid'] = transactionid
        response['txnref'] = referenceid
        transaction.txnref = referenceid
        transaction.response = result
        transaction.save()
    return responsecode, response, exception
