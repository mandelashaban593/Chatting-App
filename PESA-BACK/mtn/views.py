'''api views'''
from mtn.serializers import MtnTransactionSerializer, \
    WithdrawMoneySerializer, DepositMoneySerializer, \
    TransactionStatusSerializer
from mtn.server import Mtn
from api.utils import ApiResponse, validate_number
from api.views import ApiView
from mtn.models import MtnTransaction
from django.core import serializers
from api.network_extensions import NETWORK


def valid_msisdn(number):
    valid = False
    try:
        valid = validate_number(
            number,
            NETWORK.MTN_UGANDA
            )
    except Exception, e:
        print e
    return valid
    

class Transaction(ApiView):

    """
    DepositMoney for Mtn User number
    """
    model = MtnTransaction  # Model name
    serializer_class = MtnTransactionSerializer

    def get(self, request, transactionid=None):
        '''check if a number is registered'''
        responsecode = 0
        response = {}
        exception = None
        try:
            transactions = MtnTransaction.objects.filter(
            owner=request.user.pk
            )
            serialized_data = serializers.serialize("json",
                transactions
                )
            responsecode = 1
            response['transactions'] = serialized_data
        except Exception, e:
            exception = e
            pass
        return ApiResponse(
            responsecode, response, exception
            )


class TransactionStatus(ApiView):
    '''
    Transaction status
    '''
    serializer_class = TransactionStatusSerializer
    queryset = {}

    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        '''
        post to user
        '''
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            responsecode = 0
        else:
            response['errors'] = serializer.errors
        return ApiResponse(
            responsecode, response
            )


class WithdrawMoney(ApiView):
    '''
    Withdraw money from Mtn number
    push-pull
    '''
    serializer_class = WithdrawMoneySerializer
    queryset = {}

    def post(self, request):
        '''
        post to user
        '''
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            responsecode = 0
        else:
            response['errors'] = serializer.errors
        return ApiResponse(
            responsecode, response
            )


class DepositMoney(ApiView):

    """
    DepositMoney for Mtn number
    """
    serializer_class = DepositMoneySerializer
    queryset = {}

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
            if not valid_msisdn(msisdn):
                responsecode = 6
            else:
                responsecode, response, exception = MtnDepositMoney(msisdn, amount, request.user)
        else:
            responsecode = 7
            response['errors'] = serializer.errors
        return ApiResponse(
            responsecode, response, exception
            )


class CheckNumber(ApiView):

    """
    check if number is on sdp or is registered
    """

    def get(self, request, msisdn, format=None):
        '''check if a number is registered'''
        response = {}
        responsecode = 0
        if not valid_msisdn(msisdn):
            responsecode = 6
        else:
            number = msisdn
            mtn = Mtn()
            is_momo, momo_response = mtn.momo_check(number)
            is_kyc = mtn.kyc_check(number)
            if is_momo and is_kyc:
                responsecode = 3
            else:
                responsecode = 2
        return ApiResponse(responsecode, response)


def MtnDepositMoney(msisdn, amount, user):
    response = {}
    mtn = Mtn()
    exception = None
    responsecode = 10
    is_momo, momo_response = mtn.momo_check(msisdn)
    is_kyc = mtn.kyc_check(msisdn)
    if not is_momo or not is_kyc:
        responsecode = 2
    else:
        try:
            transaction = MtnTransaction(
                amount=amount,
                owner=user,
                phonenumber=msisdn
            )
            transaction.save()
            transactionid = transaction.transactionid
        except Exception, e:
            exception = e
        if transactionid:
            result = mtn.DepositMoney(
                amount=amount,
                number=msisdn,
                transactionid=transactionid,
                ref_text="")
            response['result'] = result
            response['transactionid'] = transactionid
    return responsecode, response, exception
