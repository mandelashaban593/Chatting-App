from django.shortcuts import render

'''api views'''
from rest_framework import authentication, permissions, serializers, viewsets, status, generics,parsers,renderers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from pegpay.serializers import UserProfileSerializer

from rest_framework.views import View, APIView
from api.views import ApiView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import json
from django.shortcuts import HttpResponse
import utils
import pegpay_server as Pegpay
from pegpay.models import UtilityTransaction,WaterTransaction,ElectricityTransaction
from serializers import WaterTransactionSerializer,ElectricityTransactionSerializer
from forms import WaterTransactionForm,ElectricityTransactionForm
import datetime
from api.utils import ApiResponse
pegpay = Pegpay.pegpay()





class QueryAccount(ApiView):
    '''query user account'''
    parser_classes = (JSONParser,) # the parser
    permission_classes = ()

    def post(self,request):
        data = request.POST.copy()
        exception = None
        status = None
        responsecode = None

        try:
            query_customer=utils.query_account_data(request.POST)

            status = pegpay.query_customer_details(query_customer)
        except Exception as e:
            exception = e
            responsecode = 9
            pass

        if status.ResponseField6 == "0":
            responsecode=0
        else:
            responsecode=9



        response = utils.response_map(status)

        try:
            json_data = json.dumps(response)

        except Exception as e:
            #exception = e
            print 'Json Conversion error: ',str(e)


        try:
            #return HttpResponse(json.dumps(response), content_type="application/json")

            #responsecode = 0
            return ApiResponse(
                responsecode, response, exception
                )

        except Exception as e:
            print ':Return Response Error: ',str(e)




class WaterTransaction(ApiView):
    '''Water transaction'''
    model = WaterTransaction
    serializer_class = WaterTransactionSerializer

    parser_classes = (JSONParser,) # the parser
    permission_classes = ()


    def post(self,request):

        form = WaterTransactionForm()
        data = request.POST.copy()
        exception = None
        status = None
        transaction_ref = None
        responsecode = None
        #response = None
        response = {}


        form = WaterTransactionForm(data)

        if form.is_valid():

            try:
                #pass
                transaction_data = utils.transaction_data(data)
                transaction_ref = transaction_data['PostField20']
                status = pegpay.post_transaction_details(transaction_data)
            except Exception as e:
                exception = e
                #pass


            if status.ResponseField6=="0":



                try:
                    responsecode = 0
                    form_data = form.save(commit=False)
                    form_data.owner=request.user
                    form_data.added=datetime.datetime.now()
                    form_data.transaction_ref=transaction_ref
                    form_data.save()
                except Exception as e:
                    print 'TransactionForm save error: ',str(e)
            else:
                print 'unsuccessful transaction'
                response = 9

            response = utils.response_map(status)
        else:

            #response['error']='invalid parameter or parameter value'
            responsecode=7
            response['field error']=form.errors.as_json()
        try:
            #return HttpResponse(json.dumps(response), content_type="application/json")
            responsecode = 0
            return ApiResponse(
                responsecode, response, exception
                )
        except Exception as e:
            print 'Response error: ',str(e)


class ElectricityTransaction(ApiView):
    '''electricity transaction'''
    model = ElectricityTransaction
    serializer_class = ElectricityTransactionSerializer

    parser_classes = (JSONParser,) # the parser
    permission_classes = ()



    def post(self,request):
        form = ElectricityTransactionForm()
        data = request.POST.copy()
        response = {}
        transaction_ref = None
        status = None
        exception = None
        responsecode = None

        form = ElectricityTransactionForm(data)

        if form.is_valid():

            try:
                transaction_data = utils.transaction_data(data)
                transaction_ref = transaction_data['PostField20']
                status = pegpay.post_transaction_details(transaction_data)
            except Exception as e:
                exception = e
                pass



            if status.ResponseField6=="0":
                try:
                    responsecode = 0
                    form_data = form.save(commit=False)
                    form_data.owner=request.user
                    form_data.added=datetime.datetime.now()
                    form_data.transaction_ref=transaction_ref
                    form_data.save()

                    temp_status=pegpay.get_transaction_details(None)

                    utils.get_transaction_test(temp_status)



                except Exception as e:
                    print 'ElectricityTransactionForm save error: ',str(e)
            else:
                responsecode = 9
                print 'unsuccessful transaction'

            response = utils.response_map(status)
        else:

            #response = {}
            responsecode = 7
            response['field error']=form.errors.as_json()

        try:
            #return HttpResponse(json.dumps(response), content_type="application/json")
            return ApiResponse(
                responsecode, response, exception
                )

        except Exception as e:
            print 'Response error: ',str(e)




    def post(self,request):

        data = request.POST.copy()
        exception = None
        status = None
        transaction_ref = None
        responsecode = None
        response = {}

        transaction_data = utils.get_transaction_data(data)

        try:
            transaction_data = utils.get_transaction_data()
            status = pegpay.get_transaction_details(transaction_data)
        except Exception as e:
            raise

        if status.ResponseField6=="0":
            response_code = 0

        response = utils.response_map(status)

        try:
            return ApiResponse(
                responsecode, response, exception
                )
        except Exception as e:
            print 'Response error: ',str(e)
