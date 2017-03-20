'''default api view for remitapi'''
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, FormParser
from remitapi.authentication import ApiAuthentication
from django.conf import settings
from api.v1.serializers import *
from api.utils import ApiResponse, validate_number
from api.network_extensions import COUNTRY, NETWORK
from api.models import PaybillAccount
from pegpay.server import PegPay
from pegpay.models import UtilityTransaction
from remitapi.models import App
from firebase_cloud_msging.models import NotifsClient
from pegpay import utils
from remit_ussd.remit_ussd import RemitUssd
from tradelance.server import Tradelance
from tradelance import utils as tlance_utils
from tradelance.models import TlanceTransaction
from remitapi import settings as tlance_settings
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from pegpay.tasks import check_transaction_status
from firebase_cloud_msging.tasks import send_push_notification
#from smart.guardian import Smart
from smart.server import Smart
from pesapot_sms.server import Sms
from firebase_cloud_msging.server import FirebaseCloudMessaging
import xmltodict

import hashlib
from rwanda.server import  Rwanda
from smile.server import Smile
from impal.server import Impal
from beyonic.server import Beyonic
import json

class ApiView(APIView):
    """
    Default Api View Class
    """
    authentication_classes = (
        ApiAuthentication,
    )
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (JSONParser, FormParser)


class PaybillRouter(ApiView):
    """
    Paybill Router
    """
    #serializer_class = PaybillSerializer
    serializer_class = None

    print ':::PaybillRouter entered'


    def post(self, request):
        responsecode = 0
        response = {}
        exception = None
        bill_data= request.data.copy()
        sender = None

        if bill_data.get('billtype') == "2":
            self.serializer_class = PaybillWithAreaSerializer
        else:
            self.serializer_class = PaybillSerializer

        serializer = self.serializer_class(data=request.data)


        transaction = UtilityTransaction()
        transactionid = None
        vendor_id = None
        ussd_id = None

        if serializer.is_valid():
            area = None
            pegpay = PegPay()
            referencenum = serializer.validated_data['referencenum']
            billtype = serializer.validated_data['billtype']
            amount = serializer.validated_data['amount']
            phonenumber = serializer.validated_data['phonenumber']
            names = serializer.validated_data['names']
            message = serializer.validated_data['message']
            paymethod = serializer.validated_data['paymethod']
            #vendor_id = serializer.validated_data['vendor_id']

            #paid_by = serializer.validated_data['paid_by']
            paid_by = request.data.get('paid_by', '')

            vendor_id = request.data.get('vendor_id', '')
            useremit_id = request.data.get('useremit_id', '')
            ussd_id = request.data.get('ussd_id','')



            try:
                area = serializer.validated_data['area']
            except Exception as e:
                print 'Parameter value error: ',str(e)

            try:
                amount = int(round(float(amount)))
            except Exception, e:
                pass

            statuscode = 30

            try:
                transaction.referencenum=referencenum
                transaction.account_name=names
                transaction.billtype = billtype
                transaction.paid_by = paid_by
                transaction.paymethod = paymethod
                transaction.recipient_phone = phonenumber
                transaction.sender_message = message
                transaction.amount = amount
                transaction.added = timezone.now()
                transaction.owner = request.user

                if vendor_id:
                    transaction.vendor_id = vendor_id
                #print ':Transaction: ',str(transaction.__dict__)
                transaction.save()

                if vendor_id:
                    print ':Sender is tradelance'
                    #transactionid = str(transaction.vendor_id)
                    transactionid = str(vendor_id)
                    sender = 'tlance'

                elif ussd_id:
                    print ':Sender is tradelance'
                    transactionid = str(transaction.transactionid)
                    sender = 'tlance'

                elif useremit_id:
                    print '::Sender is useremit'
                    sender = 'useremit'
                    transactionid = str(transaction.transactionid)
                else:
                    print '::Sender is None'

                    transactionid = str(transaction.transactionid)
                    print '::None sender transaction id: ',transactionid

            except Exception as e:
                print ':Error saving bill transaction: ', str(e)

            result = pegpay.PayBill(area,
                names,
                referencenum,
                billtype,
                amount,
                phonenumber,
                paymethod,
                transactionid,
                message,
            )
            statuscode = result.get('status_code', statuscode)
            statuscode = int(statuscode)



            if statuscode == 100 or statuscode == 35 or statuscode == 12:
                responsecode = 7
                try:
                    response['errors'] = result.get(
                        'status_description',
                        '')
                except Exception, e:
                    print "Formating response error :  %s" % e
            if statuscode == 30 or statuscode == 27 or statuscode == 32 or statuscode == 28:
                responsecode = 10
            if statuscode == 21:
                responsecode = 10
            if statuscode == 1000 or statuscode == 100 or statuscode == 0:
                '''
                we have a successfull Transaction
                '''

                response['result'] = result
                try:
                    todate = datetime.datetime.now()

                    send_date = utils.send_date(todate)
                    print 'Transaction date: ',str(send_date)
                    #print ':Transaction billtype: ',str(billtype)
                    paybillaccount = PaybillAccount()
                    paybillaccount.billtype = billtype
                    paybillaccount.modified_date = datetime.datetime.now()
                    paybillaccount.vendorid = result['vendor_transaction_id']
                    paybillaccount.amount = amount
                    paybillaccount.send_date = send_date
                    paybillaccount.save()

                    if sender == 'tlance':
                        if ussd_id:
                            print ':tlance is ussd'
                            check_transaction_status.apply_async(countdown=180,kwargs={
                                'vendorid': transactionid,
                                'vendor': 'remitussd',
                                'sender_id':ussd_id
                            })
                        else:
                            print ':tlance is NOT ussd'
                            check_transaction_status.apply_async(countdown=180,kwargs={
                                'vendorid': transactionid,
                                'vendor': 'remitussd'
                            })
                    elif sender == 'useremit':
                        check_transaction_status.apply_async(countdown=180,kwargs={
                            'vendorid': transactionid,
                            'vendor': 'useremit',
                            'sender_id':useremit_id
                        })

                except Exception as e:
                    print 'PaybillAccount save failed: ',str(e)
        else:
            responsecode = 7
            response['errors'] = serializer.errors
        return ApiResponse(
            responsecode, response, exception
        )


class PaybillQueryAccountRouter(ApiView):
    """
    Paybill Router
    """
    serializer_class = PaybillQueryAccountSerializer

    def post(self, request):
        responsecode = 0
        response = {}
        exception = None
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():


            pegpay = PegPay()
            location = serializer.validated_data['location']
            billtype = serializer.validated_data['billtype']
            referencenum = serializer.validated_data['referencenum']
            companycode = None
            statuscode = 30
            billtype = int(billtype)
            companycode = billtype
            result = pegpay.AccountDetails(
                referencenum,
                companycode,
                location
            )
            try:
                statuscode = result.get('status_code', statuscode)
            except Exception, e:
                print e
                pass
            statuscode = int(statuscode)
            if statuscode == 100:
                responsecode = 7
                response['errors'] = result.get(
                    'status_description',
                    '')
            if statuscode == 102:
                responsecode = 8

            if statuscode == 30:
                responsecode = 10

            if statuscode == 0:
                '''
                we have a successful transaction
                '''
                response['result'] = result
        else:
            responsecode = 7
            response['errors'] = serializer.errors
        return ApiResponse(
            responsecode, response, exception
        )


class PaybillGetTransactionRouter(ApiView):
    '''
    Get transaction detials
    '''
    serializer_class = PaybillTransactionDetailsSerializer

    def post(self, request):
        responsecode = 0
        response = {}
        exception = None
        statuscode = None
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            pegpay = PegPay()
            vendorid = serializer.validated_data['vendorid']

            result = pegpay.TransactionDetails(vendorid)

            print ':Transaction status Response: ',str(result)

            statuscode = result.get('status_code', statuscode)

            statuscode = int(statuscode)

            if statuscode == 1000 or statuscode == 0:
                #print 'Get TransactionDetails Success!'
                response['result'] = result

            if statuscode == 100 or statuscode == 35 or statuscode == 12:
                responsecode = 7
                error = ''
                try:
                    response['errors'] = result.get(
                        'status_description',
                        '')
                except Exception as e:
                    print "Formating response error :  %s" % e

            if statuscode == 30 or statuscode == 27 or statuscode == 32 or statuscode == 28:
                responsecode = 10
            if statuscode == 21:
                responsecode = 10

            return ApiResponse(
                responsecode, response, exception
            )

        else:
            responsecode = 7
            response['errors'] = serializer.errors
        return ApiResponse(
            responsecode, response, exception
        )



class billpaymentsEodRouter(ApiView):
    """
    send billpayment EOD to pegpay
    """
    serializer_class = PaybillSerializer

    def post(self,request):
        '''
        post
        '''

class TransactionStatus(ApiView):
    """
    Route TransactionsStatus calls
    """
    print ':Transaction status view reached'
    serializer_class = TransactionStatusSerializer

    def post(self,request):
        """
        route query
        """
        print ':post data',str(request.data)
        print ':Transaction post reached'



        exception = None
        response = {}
        responsecode = 7
        serializer = self.serializer_class(data=request.data)
        utilitybill = None

        if serializer.is_valid():
            print ':Serializer valid'
            responsecode = 0
            transaction_id = serializer.validated_data['transaction_id']
            #transaction_type = serializer.validated_data['transaction_type']
            transid = int(transaction_id)
            transaction_status = None
            for utility in UtilityTransaction.objects.all():
                if utility.app_ptr.transactionid == transid:
                    print ':Utility id found'
                    print ':Utility Status: ',str(utility.status)
                    transaction_status = utility.status
                    utilitybill = utility
                else:
                    print 'utility not found'

            if utilitybill is not None:
                response['Transaction status'] = transaction_status

        else:
            print ':Serializer not valid'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode,response,exception
        )


class TradelanceDeposit(ApiView):
    '''
    tradelance deposit money to phonenumber
    '''
    serializer_class = None

    def post(self,request):
        responsecode = 0
        response = {}
        exception = None
        statuscode = 0
        post_data = request.data.copy()
        #api_key = None
        #time_stamp = None

        serializer = self.serializer_class = TradelanceDepositSerializer(data = request.data)

        transaction_data={}
        transaction = TlanceTransaction()
        transaction_id = False


        post_data = request.POST.copy()

        transaction_id = post_data.get('transaction_id', '')
        print ':transaction_id ', str(transaction_id)

        if serializer.is_valid():
            #transaction[APIUsername]=
            tradelance = Tradelance()
            todate = datetime.datetime.now()
            time_stamp =str(todate.year)+str('%02d' % todate.month)+str('%02d' % todate.hour)+str('%02d' % todate.minute)+str('%02d' % todate.second)
            key_hash = tlance_settings.TRADELANCE_PASSWORD+time_stamp
            api_key = hashlib.md5(key_hash).hexdigest()

            transaction_data['APIUsername']=tlance_settings.TRADELANCE_USERNAME
            transaction_data['APIKey']=api_key
            transaction_data['TimeStamp']=time_stamp
            transaction_data['API']="DepositFunds"
            transaction_data['MSISDN']=serializer.validated_data['receiver_number']
            transaction_data['Amount']=serializer.validated_data['amount']
            transaction_data['CurrencyCode']=serializer.validated_data['amount']

            #transaction_data['Reference']=serializer.validated_data['']
            transaction_data['IPN']="http://127.0.0.1/myapp/ipn/"
            transaction_data['Narration']='Deposit funds'

            try:
                amount = int(round(float(transaction_data['Amount'])))
                transaction.recipient_phone = transaction_data['MSISDN']
                transaction.amount = amount
                transaction.added = timezone.now()
                transaction.owner = request.user
                transaction.api=transaction_data['API']

                transaction.save()
                #transactionid
                if transaction_id:
                    transaction_data['Reference'] = str(transaction_id)
                else:
                    transaction_data['Reference'] = str(transaction.transactionid)

            except Exception as e:
                print 'Transaction error: ',str(e)

            print ':Transaction data: ',str(transaction_data)

            xml_data = tlance_utils.dictionary_to_xml("TLRequest",transaction_data)

            result = tradelance.send_xml_request(xml_data)

            print 'xml result: ',str(result)

            response = result['tlresponse']

            response = dict(response)


            try:
                statuscode = response.get('StatusCode','')
                statuscode = int(statuscode)
            except Exception as e:
                print "status code error ",str(e)

            # if statuscode == 200:
            #     responsecode = 0
            # elif statuscode == 201:
            #     responsecode = 19
            #     response['errors'] = response.get('ErrorDescription','')
            #
            # elif statuscode == 400 or statuscode == 401 or statuscode == 403:
            #     responsecode = 20
            #     response['errors'] = response.get('ErrorDescription','')




            print ':Status code: ',str(statuscode)


        else:
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )

class TradelanceRequestPayment(ApiView):
    '''
    tradelance request payment
    '''
    serializer_class = None

    def post(self,request):

        responsecode = 0
        response = {}
        exception = None
        statuscode = 0
        post_data = request.data.copy()

        serializer = self.serializer_class = TradelanceSerializer(data = request.data)

        transaction_data={}
        transaction = TlanceTransaction()
        transactionid = None

        if serializer.is_valid():
            tradelance = Tradelance()
            todate = datetime.datetime.now()
            time_stamp =str(todate.year)+str('%02d' % todate.month)+str('%02d' % todate.hour)+str('%02d' % todate.minute)+str('%02d' % todate.second)
            key_hash = tlance_settings.TRADELANCE_PASSWORD+time_stamp
            api_key = hashlib.md5(key_hash).hexdigest()

            transaction_data['APIUsername']=tlance_settings.TRADELANCE_USERNAME
            transaction_data['APIKey']=api_key
            transaction_data['TimeStamp']=time_stamp
            transaction_data['API']="RequestPayment"
            transaction_data['MSISDN']=serializer.validated_data['receiver_number']
            transaction_data['Amount']=serializer.validated_data['amount']
            transaction_data['CurrencyCode']=serializer.validated_data['amount']
            transaction_data['IPN']="http://127.0.0.1/myapp/ipn/"
            transaction_data['Narration']='Request Payment'

            try:
                amount = int(round(float(transaction_data['Amount'])))
                transaction.recipient_phone = transaction_data['MSISDN']
                transaction.amount = amount
                transaction.added = timezone.now()
                transaction.owner = request.user
                transaction.api=transaction_data['API']

                transaction.save()
                #transactionid
                transaction_data['Reference'] = str(transaction.transactionid)

            except Exception as e:
                print 'Transaction error: ',str(e)

            xml_data = tlance_utils.dictionary_to_xml("TLRequest",transaction_data)

            # result = tradelance.send_xml_request(xml_data)
            #
            # print 'xml result: ',str(result)
            #
            # response = result['tlresponse']
            #
            # response = dict(response)

            try:
                result = tradelance.send_xml_request(xml_data)

                print 'xml result: ',str(result)

                response = result['tlresponse']

                response = dict(response)
                statuscode = response.get('StatusCode','')
                statuscode = int(statuscode)
            except Exception as e:
                print "status code error ",str(e)


        else:
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )


class TradelanceTransactionStatus(ApiView):
    '''
    tradelance transaction status
    '''
    serializer_class = None

    def post(self,request):

        responsecode = 0
        response = {}
        exception = None
        statuscode = 0
        post_data = request.data.copy()

        serializer = self.serializer_class = TradelanceStatusSerializer(data = request.data)

        transaction_data={}
        transaction = TlanceTransaction()
        transactionid = None

        if serializer.is_valid():
            #
            tradelance = Tradelance()
            todate = datetime.datetime.now()
            time_stamp =str(todate.year)+str('%02d' % todate.month)+str('%02d' % todate.hour)+str('%02d' % todate.minute)+str('%02d' % todate.second)
            key_hash = tlance_settings.TRADELANCE_PASSWORD+time_stamp
            api_key = hashlib.md5(key_hash).hexdigest()

            transaction_data['APIUsername']=tlance_settings.TRADELANCE_USERNAME
            transaction_data['APIKey']=api_key
            transaction_data['TimeStamp']=time_stamp
            transaction_data['API']="TransactionStatus"
            transaction_data['Reference']=serializer.validated_data['transaction_id']

            xml_data = tlance_utils.dictionary_to_xml("TLRequest",transaction_data)

            try:
                result = tradelance.send_xml_request(xml_data)

                print 'xml result: ',str(result)

                response = result['tlresponse']

                response = dict(response)
                statuscode = response.get('StatusCode','')
                statuscode = int(statuscode)
            except Exception as e:
                print "status code error ",str(e)

        else:
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )

class Tradelancebalancecheck(ApiView):
    '''
    check tradelance account balance
    '''
    def post(self,request):
        responsecode = 0
        response = {}
        exception = None
        statuscode = 0
        post_data = request.data.copy()

        transaction_data={}
        transaction = TlanceTransaction()

        tradelance = Tradelance()
        todate = datetime.datetime.now()
        time_stamp =str(todate.year)+str('%02d' % todate.month)+str('%02d' % todate.hour)+str('%02d' % todate.minute)+str('%02d' % todate.second)
        key_hash = tlance_settings.TRADELANCE_PASSWORD+time_stamp
        api_key = hashlib.md5(key_hash).hexdigest()

        transaction_data['APIUsername']=tlance_settings.TRADELANCE_USERNAME
        transaction_data['APIKey']=api_key
        transaction_data['TimeStamp']=time_stamp
        transaction_data['API']="BalanceCheck"

        xml_data = tlance_utils.dictionary_to_xml("TLRequest",transaction_data)

        try:
            result = tradelance.send_xml_request(xml_data)

            print 'xml result: ',str(result)

            response = result['tlresponse']

            response = dict(response)
            statuscode = response.get('StatusCode','')
            statuscode = int(statuscode)
        except Exception as e:
            print "status code error ",str(e)

        return ApiResponse(
            responsecode, response, exception
        )


class TradelanceAccountStatement(ApiView):
    '''
    Get accont statement
    '''
    serializer_class = None


    def post(self,request):

        responsecode = 0
        response = {}
        exception = None
        statuscode = 0
        post_data = request.data.copy()

        serializer = self.serializer_class = TradelanceStatementSerializer(data = request.data)

        transaction_data={}
        transaction = TlanceTransaction()

        if serializer.is_valid():
            tradelance = Tradelance()
            todate = datetime.datetime.now()
            time_stamp =str(todate.year)+str('%02d' % todate.month)+str('%02d' % todate.hour)+str('%02d' % todate.minute)+str('%02d' % todate.second)
            key_hash = tlance_settings.TRADELANCE_PASSWORD+time_stamp
            api_key = hashlib.md5(key_hash).hexdigest()

            transaction_data['APIUsername']=tlance_settings.TRADELANCE_USERNAME
            transaction_data['APIKey']=api_key
            transaction_data['TimeStamp']=time_stamp
            transaction_data['API']="AccountStatement"
            transaction_data['Account']=serializer.validated_data['account']
            transaction_data['StartDate']=serializer.validated_data['startdate']
            transaction_data['EndDate']=serializer.validated_data['enddate']

            xml_data = tlance_utils.dictionary_to_xml("TLRequest",transaction_data)

            try:
                result = tradelance.send_xml_request(xml_data)

                print 'xml result: ',str(result)

                response = result['tlresponse']

                response = dict(response)
                statuscode = response.get('StatusCode','')
                statuscode = int(statuscode)
            except Exception as e:
                print "status code error ",str(e)



        else:
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )

class TradelanceFundsTransfer(ApiView):
    """
    transfer funds to subscribers mobile account
    """
    serializer_class = None

    def post(self,request):

        responsecode = 0
        response = {}
        exception = None
        statuscode = 0
        post_data = request.data.copy()

        serializer = self.serializer_class = TradelanceTransferSerializer(data = request.data)

        transaction_data={}
        transaction = TlanceTransaction()
        transactionid = None

        if serializer.is_valid():
            #
            tradelance = Tradelance()
            todate = datetime.datetime.now()
            time_stamp =str(todate.year)+str('%02d' % todate.month)+str('%02d' % todate.hour)+str('%02d' % todate.minute)+str('%02d' % todate.second)
            key_hash = tlance_settings.TRADELANCE_PASSWORD+time_stamp
            api_key = hashlib.md5(key_hash).hexdigest()

            transaction_data['APIUsername']=tlance_settings.TRADELANCE_USERNAME
            transaction_data['APIKey']=api_key
            transaction_data['TimeStamp']=time_stamp
            transaction_data['API']="FundsTransfer"
            transaction_data['Benificiary']=serializer.validated_data['benificiary']
            transaction_data['Amount']=serializer.validated_data['amount']
            transaction_data['Narration']="Transfer funds"

            try:
                amount = int(round(float(transaction_data['Amount'])))

                transaction.amount = amount
                transaction.added = timezone.now()
                transaction.owner = request.user
                transaction.api=transaction_data['API']

                transaction.save()
                #transactionid
                transaction_data['Reference'] = str(transaction.transactionid)
            except Exception as e:
                print 'Transaction error: ',str(e)

            xml_data = tlance_utils.dictionary_to_xml("TLRequest",transaction_data)

            try:
                result = tradelance.send_xml_request(xml_data)

                print 'xml result: ',str(result)

                response = result['tlresponse']

                response = dict(response)
                statuscode = response.get('StatusCode','')
                statuscode = int(statuscode)
            except Exception as e:
                print "status code error ",str(e)

        else:
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )





class DepositMoneyRouter(ApiView):
    """
    Route DepositMoney Calls
    """
    serializer_class = DepositMoneySerializer

    def post(self, request):
        '''
        route query
        '''
        exception = None
        response = {}
        responsecode = 7
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            responsecode = 0
            msisdn = serializer.validated_data['msisdn']
            amount = serializer.validated_data['amount']
            valid, responsecode, countrycode, networkcode = validate_number(
                msisdn)
            print valid, responsecode
            if not valid:
                if responsecode == 12:
                    response['errors'] = {
                        'The country code %s is not supported' % countrycode}
                elif responsecode == 13:
                    response['errors'] = {'The network code %s is not supported for country code %s' % (
                        networkcode,
                        countrycode
                    )}
            else:
                if countrycode == COUNTRY.UGANDA:
                    '''dealing with uganda'''
                    if networkcode in NETWORK.MTN_UGANDA:
                        from mtn.views import MtnDepositMoney
                        responsecode, response, exception = MtnDepositMoney(
                            msisdn, amount, request.user)
                if countrycode == COUNTRY.KENYA:
                    '''dealing with kenya'''
                    from ipay.views import IpayDepositMoney
                    responsecode, response, exception = IpayDepositMoney(
                        msisdn, amount, request.user)
                if countrycode == COUNTRY.RWANDA:
                    '''dealing with rwanda'''
                    from rwanda.views import RwandaDepositMoney
                    responsecode, response, exception = RwandaDepositMoney(
                        msisdn, amount, request.user)
        else:
            response['errors'] = serializer.errors
        return ApiResponse(
            responsecode, response, exception
        )


class PaybillQueryTvBouquet(ApiView):
    """query payTv Bouquets."""
    print ':View reached'
    serializer_class = PaybillQueryTvBouquetSerializer

    def post(self, request):
        responsecode = 0
        response = {}
        exception = None
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            pegpay = PegPay()
            pay_tv = serializer.validated_data['pay_tv']

            result = pegpay.paytv_bouquets(pay_tv)

        return ApiResponse(
            responsecode, response, exception
        )

class SmartGuardian(ApiView):
    """make smart request."""
    serializer_class = SmartGuardianSerializer


    def post(self,request):
        print ':Smart post'
        responsecode = 0
        response = {}
        exception = None
        post_data = request.data.copy()

        request_type = post_data.get('request_type','')

        if not request_type:
            responsecode = 7
            response['errors'] = 'request_type field is required'
            return ApiResponse(
                responsecode, response, exception
            )

        print ':Method type: ', str(request_type)

        serializer = self.serializer_class(data=request.data)
        smart_dict = None

        if serializer.is_valid():
            print ':Valid smart serializer'
            smart = Smart()
            smart_data =serializer.validated_data['smart_data']
            print ':SMart data: ',str(smart_data)
            #method_type = serializer.validated_data['slay']
            #print ':Method type: ',str(method_type)



            try:
                #convert string to dict
                import ast
                smart_dict = ast.literal_eval(smart_data)
                print ':String to dict success ',str(type(smart_dict))
                print ':name ', str(smart_dict['name'])
            except Exception as e:
                print ':string to dict fail ',str(e)
            result = smart.create_request(request_type,smart_dict)


            #response_data = result.__dict__
            #response_data = xmltodict.parse(result.text)
            response_data = str(result)

            print ':Smart response data ',str(response_data)

            response['result'] = response_data
        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )

class SmartPayments(ApiView):
    """Smart spPayment."""
    serializer_class = SmartPaymentsSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        smart_data = {}

        if serializer.is_valid():
            print ':Valid serializer'
            smart = Smart()
            number = serializer.validated_data['number']
            amount = serializer.validated_data['amount']
            smart_data['subsmobileNo'] = serializer.validated_data['number']
            smart_data['amount'] = serializer.validated_data['amount']

            smart_response = smart.smart_request(smart_data, request, 0)

            print ':Smart View REsponse: ',str(smart_response)

            response['result'] = smart_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )


class SmartTransStatus(ApiView):
    """smart spCheckTransStatus."""

    serializer_class = SmartTransStatusSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        smart_data = {}

        if serializer.is_valid():
            smart = Smart()
            smart_data['uuid'] = serializer.validated_data['transaction_id']
            smart_response = smart.smart_request(smart_data, request, 1)
            print ':Smart View REsponse: ',str(smart_response)
            response['result'] = smart_response
        else:
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )

class SmartWithdrawDeposit(ApiView):
    """smart spWithdrawDeposit."""
    serializer_class = SmartWithdrawDepositSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        smart_data = {}

        if serializer.is_valid():
            smart = Smart()
            smart_data['requesttype'] = serializer.validated_data['requesttype']
            smart_data['subsmobileNo'] = serializer.validated_data['number']
            smart_data['amount'] = serializer.validated_data['amount']

            smart_response = smart.smart_request(smart_data, request, 2)

        else:
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )

class SmartSendReceiveMoney(ApiView):
    """smart spSendReceiveMoney."""
    serializer_class = SmartSendReceiveMoneySerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        smart_data = {}

        if serializer.is_valid():
            smart = Smart()
            smart_data['subsmobileNo'] = serializer.validated_data['number']
            smart_data['amount'] = serializer.validated_data['amount']

            smart_response = smart.smart_request(smart_data, request, 3)

        else:
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )


class SmartAirtimeTopup(ApiView):
    """smart spAirtimeTopup."""
    serializer_class = SmartAirtimeTopupSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        smart_data = {}

        if serializer.is_valid():
            smart = Smart()
            smart_data['subsmobileNo'] = serializer.validated_data['sender_number']
            smart_data['csubsmobileNo'] = serializer.validated_data['reciever_number']
            smart_data['amount'] = serializer.validated_data['amount']

            smart_response = smart.smart_request(smart_data, request, 4)

            print ':Smart REsponse:: ',str(smart_response)
            response['result'] = str(smart_response)

        else:
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )

class ResidentClientSmsRouter(ApiView):
    """send resident client sms."""
    serializer_class = ResidentClientSmsSerializer

    def post(self,request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        sms_response = None

        if serializer.is_valid():
            print ':Serializer valid'
            sms = Sms()
            to = serializer.validated_data['to']
            print 'to ',to
            sms_message = serializer.validated_data['sms_message']
            print 'message: ',sms_message
            sms_client = serializer.validated_data['sms_client']
            print 'sms client ',sms_client
            sms_agent = serializer.validated_data['sms_agent']
            print 'sms agent ',sms_agent

            try:
                # response = sms.send_sms(
                #     to,
                #     sms_message,
                #     sms_client,
                #     sms_agent
                # )
                sms_response = sms.send_sms(
                    to,
                    sms_message,
                    sms_client,
                    sms_agent
                )
                responsecode = 0
                print '::Sms response ',str(sms_response)
                response['result'] = 'sms added to send cue'
            except Exception as e:
                print ':Send sms failed ',str(e)
                responsecode = 7
                #response['errors'] = str(e)
                #response['errors'] = 'A problem has occured on our end.'
        else:
            print ':Serializer invalid'
            responsecode = 7
            response['errors'] = serializer.errors
        return ApiResponse(
            responsecode, response, exception
        )

class ClientSmsRouter(ApiView):
    """send client sms."""
    serializer_class = ClientSmsSerializer

    def post(self,request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        sms_response = {}

        if serializer.is_valid():
            print ':Serializer valid'

            #sms = Sms()
        else:
            print ':Serializer invalid'
            responsecode = 7
            response['errors'] = serializer.errors
        return ApiResponse(
            responsecode, response, exception
        )


class RegisterNotifClientRouter(ApiView):
    """register notification client."""
    serializer_class = RegisterNotifsClientSerializer

    def post(self,request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        client_id = False

        if serializer.is_valid():
            print ':Serializer Valid'

            try:
                notifs_client = NotifsClient()
                user = request.user
                client_name = serializer.validated_data['client_name'].lower()
                client_key = serializer.validated_data['client_key']
                notifs_client.client_name = client_name
                notifs_client.api_key = client_key
                notifs_client.user = user
                notifs_client.save()
                client_id = notifs_client.client_id
                print ':Register Success: ',str(client_id)
                response['client_id'] = client_id
            except Exception as e:
                print ':Register error ',str(e)
                print ':Register error object ',str(e.__dict__)

                error_value = str(e).split('.')[-1]

                if error_value.lower() == 'client_name':
                    responsecode = 22
                elif error_value.lower() == 'api_key':
                    responsecode = 21

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )




class RwandaQueryAccount(ApiView):
    """Smart spPayment."""
    serializer_class = RwandaQueryAccountSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        rwanda_data = {}

        transaction = UtilityTransaction()

        if serializer.is_valid():
            print ':Valid serializer'
            rwanda = Rwanda()
            rwanda_data['mt_msgtype'] = serializer.validated_data['mt_msgtype']
            mt_msgtype = rwanda_data['mt_msgtype']
            transaction.sender_message = mt_msgtype
            transaction.amount = 0
            transaction.owner = request.user
            transaction.save()
            rwanda_data['mi_msgid'] = transaction.transactionid


            rwanda_response =rwanda.QueryAccount(rwanda_data)

            print ':Rwanda  View REsponse: ',str(rwanda_response)

            response['result'] = rwanda_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )


class RwandaEnquirePayment(ApiView):
    """Smart spPayment."""
    serializer_class = RwandaEnquirePaymentSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        rwanda_data = {}
        transaction = UtilityTransaction()

        if serializer.is_valid():
            print ':Valid serializer'
            rwanda = Rwanda()


            rwanda_data['productRef'] = serializer.validated_data['productRef']
            rwanda_data['consumerRef'] = serializer.validated_data['consumerRef']
            rwanda_data['mt_msgtype'] = serializer.validated_data['mt_msgtype']
            rwanda_data['amount'] = serializer.validated_data['amount']

            consumerRef = rwanda_data['consumerRef']
            transaction.sender_message = consumerRef
            transaction.amount = rwanda_data['amount']
            transaction.owner = request.user
            transaction.save()
            rwanda_data['mi_msgid'] = transaction.transactionid

            rwanda_response =rwanda.EnquirePayment(rwanda_data)

            print ':Rwanda  View REsponse: ',str(rwanda_response)

            response['result'] = rwanda_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )








class RwandaConfirmPayment(ApiView):
    """Smart spPayment."""
    serializer_class = RwandaEnquirePaymentSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        rwanda_data = {}
        transaction = UtilityTransaction()

        if serializer.is_valid():
            print ':Valid serializer'
            rwanda = Rwanda()

            rwanda_data['productRef'] = serializer.validated_data['productRef']
            rwanda_data['consumerRef'] = serializer.validated_data['consumerRef']
            rwanda_data['mt_msgtype'] = serializer.validated_data['mt_msgtype']
            rwanda_data['amount'] = serializer.validated_data['amount']

            consumerRef = rwanda_data['consumerRef']
            transaction.sender_message = consumerRef
            transaction.amount = rwanda_data['amount']
            transaction.owner = request.user
            transaction.save()
            rwanda_data['mi_msgid'] = transaction.transactionid

            rwanda_response =rwanda.EnquirePayment(rwanda_data)

            print ':Rwanda  View REsponse: ',str(rwanda_response)

            response['result'] = rwanda_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )




class RwandaRetryPayment(ApiView):
    """Smart spPayment."""
    serializer_class = RwandaRetryPaymentSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        rwanda_data = {}


        if serializer.is_valid():
            print ':Valid serializer'
            rwanda = Rwanda()
            rwanda_data['mi_msgid'] = serializer.validated_data['mi_msgid']
            rwanda_data['mt_msgtype'] = serializer.validated_data['mt_msgtype']

            rwanda_response =rwanda.RetryPayment(rwanda_data)

            print ':Rwanda  View REsponse: ',str(rwanda_response)

            response['result'] = rwanda_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )




class RwandaReissuePayment(ApiView):
    """Smart spPayment."""

    """Smart spPayment."""
    serializer_class = RwandaReissuePaymentSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        rwanda_data = {}

        if serializer.is_valid():
            print ':Valid serializer'
            rwanda = Rwanda()
            rwanda_data['mt_msgtype'] = serializer.validated_data['mt_msgtype']
            rwanda_data['receiptRef'] = serializer.validated_data['receiptRef']
            rwanda_response =rwanda.ReissuePayment(rwanda_data)

            print ':Rwanda View REsponse: ',str(rwanda_response)

            response['result'] = rwanda_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )



class RwandaPaymentMiniHistoryPerProduct(ApiView):
    """Smart spPayment."""

    """Smart spPayment."""
    serializer_class = RwandaPaymentMiniHistoryPerProductSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        rwanda_data = {}

        if serializer.is_valid():
            print ':Valid serializer'
            rwanda = Rwanda()
            rwanda_data['messageId'] = serializer.validated_data['messageId']
            rwanda_data['userLanguage'] = serializer.validated_data['userLanguage']
            rwanda_data['offset'] = serializer.validated_data['offset']
            rwanda_data['maxNoItems'] = serializer.validated_data['maxNoItems']
            rwanda_data['productRef '] = serializer.validated_data['productRef']

            rwanda_response =rwanda.PaymentMiniHistoryPerProduct(rwanda_data)

            print ':Rwanda View REsponse: ',str(rwanda_response)

            response['result'] = rwanda_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )


class RwandaGetTodayMiniReport(ApiView):
    """Smart spPayment."""
    serializer_class = RwandaGetTodayMiniReportSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        rwanda_data = {}

        if serializer.is_valid():
            print ':Valid serializer'
            rwanda = Rwanda()
            rwanda_data['mt_msgtype'] = serializer.validated_data['mt_msgtype']

            rwanda_response =rwanda.GetTodayMiniReport(rwanda_data)

            print ':Rwanda View REsponse: ',str(rwanda_response)

            response['result'] = rwanda_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )


class RwandaGetDailyMiniReport(ApiView):
    """Smart spPayment."""
    serializer_class = RwandaGetDailyMiniReportSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        rwanda_data = {}

        if serializer.is_valid():
            print ':Valid serializer'
            rwanda = Rwanda()
            rwanda_data['mt_msgtype'] = serializer.validated_data['mt_msgtype']
            rwanda_data['day'] = serializer.validated_data['day']


            rwanda_response =rwanda.GetDailyMiniReport(rwanda_data)

            print ':Rwanda View REsponse: ',str(rwanda_response)

            response['result'] = rwanda_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )







class RwandaGetThisMonthMiniReport(ApiView):
    """Smart spPayment."""

    """Smart spPayment."""
    serializer_class = RwandaGetThisMonthMiniReportSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        rwanda_data = {}

        if serializer.is_valid():
            print ':Valid serializer'
            rwanda = Rwanda()
            rwanda_data['mt_msgtype'] = serializer.validated_data['mt_msgtype']

            rwanda_response =rwanda.GetMonthlyMiniReport(rwanda_data)

            print ':Rwanda View REsponse: ',str(rwanda_response)

            response['result'] = rwanda_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )

class SmileAuthenticate(ApiView):
    """Smart spPayment."""
    serializer_class = SmileAuthenticateSerializer
    SessionId = ""
    smile_response = {}

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        smile_data = {}

        if serializer.is_valid():
            print ':Valid serializer'
            smile = Smile()
            smile_data['Username'] = serializer.validated_data['Username']
            smile_data['Password'] = serializer.validated_data['Password']

            smile_response = smile.smile_auth_request(smile_data, request, 0)
            
            print ':Smart View REsponse: ',str(smile_response)

            response['result'] = smile_response

            
            

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )

class SmileBalanceQuery(ApiView):
    """Smart spPayment."""
    serializer_class = SmileBalanceQuerySerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        smile_data = {}

        if serializer.is_valid():
            print ':Valid serializer'
            smile = Smile()

            

            smile_data['AccountId'] = serializer.validated_data['AccountId']

            smile_response = smile.smile_request_bal(smile_data, request, 1)

            print ':Smart View REsponse: ',str(smile_response)

            response['result'] = smile_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )


class SmileBalanceTransfer(ApiView):
    """Smart spPayment."""
    serializer_class = SmileBalanceTransferSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        smile_data = {}
        transaction = UtilityTransaction()

        if serializer.is_valid():
            print ':Valid serializer'
            smile = Smile()
            smile_data['FromAccountId'] = "2081908231"
            smile_data['ToAccountId'] = serializer.validated_data['ToAccountId']
            smile_data['TransferAmountInCents'] = serializer.validated_data['TransferAmountInCents']
            FromAccountId = smile_data['FromAccountId']
            transaction.sender_message = FromAccountId
            transaction.amount = smile_data['TransferAmountInCents']
            transaction.owner = request.user
            transaction.save()
            smile_data['UniqueTransactionId'] = transaction.transactionid

            smile_response = smile.smile_request_baltrans(smile_data, request, 2)

            print ':Smart View REsponse: ',str(smile_response)

            response['result'] = smile_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )



class SmileValidateAccountQuery(ApiView):
    """Smart spPayment."""
    serializer_class = SmileValidateAccountQuerySerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        smile_data = {}

        if serializer.is_valid():
            print ':Valid serializer'
            smile = Smile()
            
            smile_data['AccountId'] = serializer.validated_data['AccountId']

            smile_response = smile.request_valacct(smile_data, request, 3)

            print ':Smile View REsponse: ',str(smile_response)

            response['result'] = smile_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )


class SmileBundleCatalogueQuery(ApiView):
    """Smart spPayment."""
    

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        
        smile_data = {}

        
        print ':Valid serializer'
        smile = Smile()
        smile_response = smile.smile_request_cat(smile_data, request, 4)

        print ':Smile View REsponse: ',str(smile_response)

        response['result'] = smile_response

        return ApiResponse(
            responsecode, response, exception
        )




class SmileBuyBundle(ApiView):
    """Smart spPayment."""
    serializer_class = SmileBuyBundleSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        smile_data = {}
        transaction = UtilityTransaction()

        if serializer.is_valid():
            print ':Valid serializer'
            smile = Smile()
            smile_data['SessionId'] = request.session['SessionId']
            smile_data['BundleTypeCode'] = serializer.validated_data['BundleTypeCode']
            smile_data['CustomerAccountId'] = serializer.validated_data['CustomerAccountId']
            smile_data['QuantityBought'] = serializer.validated_data['QuantityBought']
            smile_data['CustomerTenderedAmountInCents'] = serializer.validated_data['CustomerTenderedAmountInCents']
            CustomerAccountId = smile_data['CustomerAccountId']
            transaction.sender_message = CustomerAccountId
            transaction.amount = smile_data['QuantityBought']
            transaction.beyon_sender = 0
            transaction.owner = request.user
            transaction.save()
            smile_data['UniqueTransactionId'] = transaction.transactionid
            smile_response = smile.buybundle(smile_data, request, 5)

            print ':Smile View REsponse: ',str(smile_response)

            response['result'] = smile_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )




class SmileTransactionStatusQuery(ApiView):
    """Smart spPayment."""
    serializer_class = SmileTransactionStatusQuerySerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        smile_data = {}
        transaction = UtilityTransaction()

        if serializer.is_valid():
            print ':Valid serializer'
            smile = Smile()
            smile_data['UniqueTransactionId'] = serializer.validated_data['UniqueTransactionId']

            smile_response = smile.trans_status(smile_data, request, 6)

            print ':Smile View REsponse: ',str(smile_response)

            response['result'] = smile_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )



class SmileNewCustomer(ApiView):
    """Smart spPayment."""
    serializer_class = SmileNewCustomerSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        smile_data = {}
        transaction = UtilityTransaction()

        if serializer.is_valid():
            print ':Valid serializer'
            smile = Smile()
            smile_data['SessionId'] = request.session['SessionId']
            smile_data['FirstName'] = serializer.validated_data['FirstName']
            smile_data['MiddleName'] = serializer.validated_data['MiddleName']
            smile_data['LastName'] = serializer.validated_data['LastName']
            smile_data['IdentityNumber'] = serializer.validated_data['IdentityNumber']
            smile_data['IdentityNumberType'] = serializer.validated_data['IdentityNumberType']
            smile_data['Line1'] = serializer.validated_data['Line1']
            smile_data['Line2'] = serializer.validated_data['Line2']
            smile_data['Zone'] = serializer.validated_data['Zone']
            smile_data['Town'] = serializer.validated_data['Town']
            smile_data['State'] = serializer.validated_data['State']
            smile_data['Country'] = serializer.validated_data['Country']
            smile_data['Code'] = serializer.validated_data['Code']
            smile_data['Type'] = serializer.validated_data['Type']
            smile_data['PostalMatchesPhysical'] = serializer.validated_data['PostalMatchesPhysical']
            smile_data['DateOfBirth'] = serializer.validated_data['DateOfBirth']
            smile_data['Gender'] = serializer.validated_data['Gender']
            smile_data['Language'] = serializer.validated_data['Language']
            smile_data['EmailAddress'] = serializer.validated_data['EmailAddress']
            smile_data['AlternativeContact1'] = serializer.validated_data['AlternativeContact1']
            smile_data['AlternativeContact2'] = serializer.validated_data['AlternativeContact2']
            smile_data['MothersMaidenName'] = serializer.validated_data['MothersMaidenName']
            smile_data['Nationality'] = serializer.validated_data['Nationality']
            smile_data['PassportExpiryDate'] = serializer.validated_data['PassportExpiryDate']

            smile_response = smile.newcustomer(smile_data, request, 7)

            print ':Smile View REsponse: ',str(smile_response)

            response['result'] = smile_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )



class SmileValidateReferenceId(ApiView):
    """Smart spPayment."""
    serializer_class = SmileValidateReferenceIdSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        smile_data = {}

        if serializer.is_valid():
            print ':Valid serializer'
            smile = Smile()

            smile_data['SessionId'] = request.session['SessionId']

            smile_data['ReferenceId'] = serializer.validated_data['ReferenceId']

            smile_response = smile.valref(smile_data, request, 8)

            print ':Smile View REsponse: ',str(smile_response)

            response['result'] = smile_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )

class SmileValidateEmailAddress(ApiView):
    """Smart spPayment."""
    serializer_class = SmileValidateEmailAddressSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        smile_data = {}

        if serializer.is_valid():
            print ':Valid serializer'
            smile = Smile()
            smile_data['EmailAddress'] = serializer.validated_data['EmailAddress']

            smile_response = smile.valemail(smile_data, request, 9)

            print ':Smile View REsponse: ',str(smile_response)

            response['result'] = smile_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )


class SmileValidatePhone(ApiView):
    """Smart spPayment."""
    serializer_class = SmileValidatePhoneSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        smile_data = {}

        if serializer.is_valid():
            print ':Valid serializer'
            smile = Smile()
            smile_data['SessionId'] = request.session['SessionId']
            smile_data['PhoneNumber'] = serializer.validated_data['PhoneNumber']

            smile_response = smile.valephone(smile_data, request, 10)

            print ':Smile View REsponse: ',str(smile_response)

            response['result'] = smile_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )




class ImpalRequestDemo(ApiView):
    """Smart spPayment."""

    """Smart spPayment."""
    serializer_class = ImpalRequestDemoSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        impal_data = {}

        if serializer.is_valid():
            print ':Valid serializer'
            Impal = Impal()
            impal_data['api_username'] = serializer.validated_data['api_username']
            impal_data['api_password'] = serializer.validated_data['api_password']
            impal_response =impal.RequestDemo(impal_data)

            print ':Impal View REsponse: ',str(impal_response)

            response['result'] = impal_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )

class ImpalReqSesid(ApiView):
    """Smart spPayment."""

    """Smart spPayment."""
    serializer_class = ImpalRequestDemoSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        impal_data = {}

        if serializer.is_valid():
            print ':Valid serializer'
            Impal = Impal()
            impal_data['api_username'] = serializer.validated_data['api_username']
            impal_data['api_password'] = serializer.validated_data['api_password']
            impal_response =impal.ReqSesid(impal_data)

            print ':Impal View REsponse: ',str(impal_response)

            response['result'] = impal_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )

class ImpalSendMoney(ApiView):
    """Smart spPayment."""

    """Smart spPayment."""
    serializer_class = ImpalSendMoneySerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        impal_data = {}

        if serializer.is_valid():
            print ':Valid serializer'
            Impal = Impal()
            impal_data['session_id'] = serializer.validated_data['session_id']
            impal_data['source_country_code'] = serializer.validated_data['source_country_code']
            impal_data['sendername'] = serializer.validated_data['sendername']
            impal_data['recipient_mobile'] = serializer.validated_data['api_password']
            impal_data['amount'] = serializer.validated_data['amount']
            impal_data['recipient_currency_code'] = serializer.validated_data['recipient_currency_code']
            impal_data['recipient_country_code '] = serializer.validated_data['recipient_country_code ']
            impal_data['reference_number'] = serializer.validated_data['reference_number']
            impal_data['sendertoken '] = serializer.validated_data['sendertoken']

            impal_response =impal.mnoTransfer(impal_data)
            print ':Impal View REsponse: ',str(impal_response)

            response['result'] = impal_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )


class ImpalBankTransfer(ApiView):
    """Smart spPayment."""

    """Smart spPayment."""
    serializer_class = ImpalBankTransferSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        impal_data = {}

        if serializer.is_valid():
            print ':Valid serializer'
            Impal = Impal()
            impal_data['session_id'] = serializer.validated_data['session_id']
            impal_data['source_country_code'] = serializer.validated_data['source_country_code']
            impal_data['sendername'] = serializer.validated_data['sendername']
            impal_data['recipient_mobile'] = serializer.validated_data['recipient_mobile']
            impal_data['recipient_currency_code'] = serializer.validated_data['recipient_currency_code']
            impal_data['recipient_country_code '] = serializer.validated_data['recipient_country_code ']
            impal_data['reference_number'] = serializer.validated_data['reference_number']
            impal_data['bank_code'] = serializer.validated_data['bank_code']
            impal_data['amount'] = serializer.validated_data['amount']
            impal_data['sender_address'] = serializer.validated_data['sender_address']
            impal_data['sender_city'] = serializer.validated_data['sender_city']
            impal_data['recipientname'] = serializer.validated_data['recipientname']
            impal_data['accountnumber'] = serializer.validated_data['accountnumber']

            impal_response =impal.BankTransfer(impal_data)
            print ':Impal View REsponse: ',str(impal_response)

            response['result'] = impal_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )

class ImpalBalance(ApiView):
    """Smart spPayment."""

    """Smart spPayment."""
    serializer_class = ImpalBalanceSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        impal_data = {}

        if serializer.is_valid():
            print ':Valid serializer'
            Impal = Impal()
            impal_data['session_id'] = serializer.validated_data['session_id']

            impal_response =impal.Balance(impal_data)
            print ':Impal View REsponse: ',str(impal_response)

            response['result'] = impal_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )



class ImpalTranStaus(ApiView):
    """Smart spPayment."""

    """Smart spPayment."""
    serializer_class = ImpalTranStausSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        impal_data = {}

        if serializer.is_valid():
            print ':Valid serializer'
            Impal = Impal()
            impal_data['reference_number '] = serializer.validated_data['reference_number']

            impal_response =impal.TranStaus(impal_data)
            print ':Impal View REsponse: ',str(impal_response)

            response['result'] = impal_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )



class ImpalXRate(ApiView):
    """Smart spPayment."""

    """Smart spPayment."""
    serializer_class = ImpalXRateSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        client_id = False

        if serializer.is_valid():
            print ':Serializer Valid'

            try:
                notifs_client = NotifsClient()
                user = request.user
                client_name = serializer.validated_data['client_name'].lower()
                client_key = serializer.validated_data['client_key']
                notifs_client.client_name = client_name
                notifs_client.api_key = client_key
                notifs_client.user = user
                notifs_client.save()
                client_id = notifs_client.client_id
                print ':Register Success: ',str(client_id)
                response['client_id'] = client_id
            except Exception as e:
                print ':Register error ',str(e)
                print ':Register error object ',str(e.__dict__)

                error_value = str(e).split('.')[-1]

                if error_value.lower() == 'client_name':
                    responsecode = 22
                elif error_value.lower() == 'api_key':
                    responsecode = 21

                #response['errors'] = str(e)


            #response['result'] = 'valid serializer'
        impal_data = {}

        if serializer.is_valid():
            print ':Valid serializer'
            Impal = Impal()
            impal_data['session_id '] = serializer.validated_data['session_id']
            impal_data['fromct'] = serializer.validated_data['fromct']
            impal_data['to'] = serializer.validated_data['to']

            impal_response =impal.XRate(impal_data)
            print ':Impal View REsponse: ',str(impal_response)

            response['result'] = impal_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )

class ImpalVerifyBen(ApiView):
    """Smart spPayment."""

    """Smart spPayment."""
    serializer_class = ImpalVerifyBenSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        impal_data = {}

        if serializer.is_valid():
            print ':Valid serializer'
            Impal = Impal()
            impal_data['session_id '] = serializer.validated_data['session_id']
            impal_data['first_name'] = serializer.validated_data['first_name']
            impal_data['second_name'] = serializer.validated_data['second_name']
            impal_data['last_name '] = serializer.validated_data['last_name']
            impal_data['mobile_number'] = serializer.validated_data['mobile_number']
            impal_data['country_code'] = serializer.validated_data['country_code']

            impal_response =impal.verifybeneficiary(impal_data)
            print ':Impal View REsponse: ',str(impal_response)

            response['result'] = impal_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )


class SendMobileNotifRouter(ApiView):
    """send push notification."""
    serializer_class = SendMobileNotifSerializer

    def post(self,request):
        exception = None
        response = {}
        responsecode = 0
        push_notif = {}
        client_key = False
        #data_message = False
        serializer = self.serializer_class(data=request.data)

        post_data = request.data.copy()

        data_message = post_data.get('data_message','')

        if serializer.is_valid():
            print ':Valid serializer'
            fcm = FirebaseCloudMessaging()
            message_title = serializer.validated_data['message_title']
            message_body = serializer.validated_data['message_body']
            reg_id = serializer.validated_data['reg_id']
            client_id = serializer.validated_data['client_id']


            try:
                str_id = str(client_id)
                id = int(str_id) ^ 0xABCDEFAB
                notifs_client = NotifsClient.objects.get(id=id)

                client_key = notifs_client.api_key

                push_notif['registration_id'] = reg_id
                push_notif['message_title'] = message_title
                push_notif['message_body'] = message_body
                push_notif['api_key'] = client_key

                if data_message:
                    push_notif['data_message'] = data_message

                print ':client id success ',str(notifs_client.__dict__)

                #status = fcm.single_device(**push_notif)

                send_push_notification.apply_async(countdown=30,kwargs={
                    'data': push_notif
                })

                #response['result'] = status
                response['result'] = 'push notticication added to cue'

                #print '::Push Notif Status ',str(status)

            except Exception as e:
                print ':client id failed ',str(e)

        else:
            print ':Invalid serializer'

        return ApiResponse(
            responsecode, response, exception
        )




class ImpalmsisdnBal(ApiView):
    """Smart spPayment."""

    """Smart spPayment."""
    serializer_class = ImpalmsisdnBalSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        impal_data = {}

        if serializer.is_valid():
            print ':Valid serializer'
            Impal = Impal()
            impal_data['session_id '] = serializer.validated_data['session_id']
            impal_data['country_code'] = serializer.validated_data['country_code']

            impal_response =impal.msisdnbalance(impal_data)
            print ':Impal View REsponse: ',str(impal_response)

            response['result'] = impal_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )


class BeyonicCollectionRequests(ApiView):
    """Smart spPayment."""
    serializer_class = BeyonicCollectionRequestsSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 0
        serializer = self.serializer_class(data=request.data)
        beyonic_data = {}
        transaction = UtilityTransaction()

        if serializer.is_valid():
            print ':Valid serializer'
            beyonic = Beyonic()

            beyonic_data['phonenumber'] = serializer.validated_data['phonenumber']
            beyonic_data['currency'] = serializer.validated_data['currency']
            beyonic_data['amount'] = serializer.validated_data['amount']
            beyonic_data['my_id'] = serializer.validated_data['my_id']
            phonenumber = beyonic_data['phonenumber']
            transaction.sender_message = phonenumber
            transaction.amount = beyonic_data['amount']
            transaction.owner = request.user
            transaction.save()

            beyonic_response =beyonic.BeyonicCollectionRequests(beyonic_data)

            print ':Beyonic  View REsponse: ',str(beyonic_response)

            response['result'] = beyonic_response

        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )





class BeyonicPayments(ApiView):
    """Smart spPayment."""
    serializer_class = BeyonicPaymentsSerializer

    def post(self, request):
        exception = None
        response = {}
        responsecode = 1
        serializer = self.serializer_class(data=request.data)
        beyonic_data = {}

        try:
            bill_data= request.data.copy()
            transid = bill_data.get('transid') 
        except Exception as e:
            print "Transaction d", transid

        transaction = UtilityTransaction()
        pay_type_error = {'pay_type_error': {"pay_type_error":None}}

        if serializer.is_valid():
            print ':Valid serializer'
            beyonic = Beyonic()
            responsecode = 0
            beyonic_data['phonenumber'] = serializer.validated_data['phonenumber']
            beyonic_data['currency'] = serializer.validated_data['currency']
            beyonic_data['account'] = settings.BEYONIC_ACCOUNT
            beyonic_data['amount'] = serializer.validated_data['amount']
            beyonic_data['description'] = serializer.validated_data['description']
            beyonic_data['payment_type'] = serializer.validated_data['payment_type']
            beyonic_data['sender'] = serializer.validated_data['sender']

            if '1' in beyonic_data.values():
                beyonic_data['transid'] = transid

                print "USEREMIT TRANS ID", beyonic_data['transid'] 
                
                phonenumber = beyonic_data['phonenumber']
                transaction.sender_message = phonenumber
                transaction.amount = beyonic_data['amount']
                transaction.beyon_transid = transid
                transaction.beyon_sender = beyonic_data['sender']
                transaction.sender_name = 'Useremit'
                transaction.owner = request.user
                transaction.save()
            # rwanda_data['mi_msgid'] = transaction.transactionid

            beyonic_response =beyonic.BeyonicPayments(beyonic_data)

            print ':Beyonic  View REsponse: ', beyonic_response
            beyonic_response = str(beyonic_response)
            

            if is_json(beyonic_response):
                beyonic_response = json.loads(beyonic_response)


                Errormsg = {}
                if 'phonenumber' in  beyonic_response and not 'id' in beyonic_response:
                    Errormsg["Errormsg"] = "Invalid Phone number"
                    response["result"] = Errormsg
                    responsecode = 30

                if 'currency' in beyonic_response and  not 'id' in beyonic_response:

                    Errormsg["Errormsg"] = "Invalid currency"
                    response["result"] = Errormsg
                    responsecode = 31

                if 'account' in beyonic_response and  not 'id' in beyonic_response:

                    Errormsg["Errormsg"] = "Invalid account"
                    response["result"] = Errormsg
                    responsecode = 32

                if 'amount' in beyonic_response and  not 'id' in beyonic_response:

                    Errormsg["Errormsg"] = "Invalid amount"
                    response["result"] = beyonic_response
                    responsecode = 34




                else:
                    response['result'] = beyonic_response

            else:
                response={'result':{'pay_type_error':None}}
                

                response['result']['pay_type_error'] = pay_type_error['pay_type_error']['pay_type_error'] = "Incorrect payment type"
                responsecode = 33
                return ApiResponse(
            responsecode, response, exception
        )



        else:
            print ':Invalid serializer'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode, response, exception
        )


def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError, e:
    return False
  return True



