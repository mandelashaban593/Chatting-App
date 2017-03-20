"""
Created by Isaac
"""

import sys
import suds
from suds import client
from suds.plugin import MessagePlugin
from suds.sax.element import Element
from suds.sax.attribute import Attribute
from pegpay.utils import query_account_data,  response_map, transaction_data, get_transaction_data, query_tv_bouquets,obj_dict
import remitapi.settings as settings
from remit_ussd.remit_ussd import RemitUssd
from useremit.useremit import Useremit
from datetime import datetime
import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)
from api.models import PaybillAccount


class PegPay():

    """
    Handle payments for PegPay.
    Powered by suds [pip install suds]
    refference: https://fedorahosted.org/suds/wiki/Documentation
    """

    def __init__(self):
        self.pegpay_username = settings.PEGPAY_USERNAME
        self.pegpay_password = settings.PEGPAY_PASSWORD
        self.pegpay_url = settings.PEGPAY_URL
        # self.client = suds.client.Client(self.pegpay_url)
        self.client = None

        # isaac mods
        self.prepaid_transaction = False

    def PayBill(self,area,names,
                referencenumber, billtype,
                amount, phonenumber, paymethod,transactionid, message=None):
        if not message:
            message = "Bill Payment for Remit"
        result = {}
        account_detials = self.AccountDetails(
            referencenumber,
            billtype
        )
        billtype = int(billtype)

        paymethod = paymethod.upper()
        #print ':Inside paybill. Area: ',str(area)

        companycode = ''
        if billtype == 1:
            companycode = 'UMEME'
        elif billtype == 2:
            companycode = 'NWSC'
        elif billtype == 3:
            companycode = 'DSTV'
        elif billtype == 4:
            companycode = 'GOTV'
        elif billtype == 5:
            companycode = 'MUBS'
        elif billtype == 6:
            companycode = 'MAK'
        elif billtype == 7:
            companycode = 'KYU'
        elif billtype == 8:
            companycode = 'NKZ'

        print '::PAY BILL Transaction ID: ',str(transactionid)


        #names = 'Remit'
        #names = names.replace(" ", "")
        #area = 'Kampala'
        try:
            print 'a'
            #area = account_detials.get("area_tin", " ")
            #names = account_detials.get("customer_name", " ")
        except Exception, e:
            print e
        data = {
            'customer_ref': referencenumber,
            'customer_name': names,
            'customer_phone': phonenumber,
            'paid_by': names,
            'amount': amount,
            'sender_message': message,
            'company_code': companycode,
            #'area': area,
            'customer_email': '',
            'customer_type': 1,
            'payment_type': 1,
            'paymethod': paymethod,
            'transactionid':transactionid,
        }

        #if area isnt null add it to data
        if area is not None or area != "":

            data['area']=area

        data = transaction_data(data)

        print ':PAybill Data ',str(data)

        result = self.post_transaction_details(data)
        result = response_map(result)

        # add vendor transaction id to the response which will later be used to
        # get transaction details
        result['vendor_transaction_id'] = data.get('PostField20', '')
        return result

    def AccountDetails(self, referencenumber, companycode, location=None):
        """
        get account details
        """
        response = {}
        try:

            companycode = int(companycode)

        except Exception as e:
            print 'failed int company code: ', str(e)

        company_code = None
        # if companycode == 2:
        #     company_code = 'NWSC'
        # elif companycode == 1:
        #     company_code = 'UMEME'

        if companycode == 1:
            company_code = 'UMEME'
        elif companycode == 2:
            company_code = 'NWSC'
        elif companycode == 3:
            company_code = 'DSTV'
        elif companycode == 4:
            company_code = 'GOTV'
        elif companycode == 5:
            company_code = 'MUBS'
        elif companycode == 6:
            company_code = 'MAK'
        elif companycode == 7:
            company_code = 'KYU'
        elif companycode == 8:
            company_code = 'NKZ'


        print ':Company_Code: ',str(company_code)

        account, created = PaybillAccount.objects.get_or_create(
            billtype=companycode,
            referencenumber=referencenumber
        )
        if not company_code:
            raise AttributeError("Please provide a valid companycode (1 or 2)")

        do_not_cache = True

        if do_not_cache: #if created:
            post_data = {
                'company_code': company_code,
                'area': location,
                'customer_ref': referencenumber,
            }

            try:
                data = query_account_data(post_data)
                response_object = self.query_customer_details(data)

                print '::REsponse object ',str(response_object)

                response = response_map(response_object)
                statuscode = response.get('status_code', 30)
                statuscode = int(statuscode)
                if not statuscode == 30 or statuscode == 102:
                    account.location = location
                    account.details = response
                    account.save()
            except Exception, e:
                response['error'] = e
        #print account.details
        response = account.details
        return response

    def TransactionDetails(self, referenceid):
        '''
        Get transaction details
        '''
        print ':inside get transaction details.'
        transaction_request = {}
        data = {
            'referenceid': referenceid
        }

        transaction_data = get_transaction_data(data)

        #print 'GetTransactionDetails data: ', str(transaction_data)

        for postfield in transaction_data:
            #
            transaction_request[postfield] = transaction_data[postfield]

        # result =

        if self.client is None:
            #print ':Self.client is None'
            client_data = self.init_client()
            self.client = client_data
        else:
            #print ':Self.client not None'
            pass

        try:
            # pass
            result = self.client.service.GetTransactionDetails(
                transaction_request)

            print ':Transaction Destails pre map ',str(result)

            response = response_map(result)

            print ':Get transaction details success.'

            #print 'GetTransactionDetails response: ', str(response)

            return response
        except Exception as e:
            # raise
            print 'GetTransactionDetails Exception: ', str(e)

    def query_customer_details(self, customer_data):
        """
        Check that customer is valid.
        customer_data: dictionary containing QueryField and value.
        Supply dictionary with "QueryFieldX":"QueryFieldX_value" sets.
        where X is a value 1,2,18,etc.
        Check pegpay documentation for QueryField specifics.
        """
        # self.client = suds.client.Client(self.pegpay_url)

        # create QueryRequest instance
        if self.client is None:
            #print ':Self.client is None'
            client_data = self.init_client()
            self.client = client_data
        else:
            #print ':Self.client not None'
            pass

        # client = self.init_client()
        query_request = self.client.factory.create('QueryRequest')
        # query_request = client.factory.create('QueryRequest')
        #print ':Query Request: ', str(query_request)

        # Iterate customer_data dictionary,asighn QueryField values
        for queryfield in customer_data:
            query_request[queryfield] = customer_data[queryfield]

        # query customer details and return response
        return self.client.service.QueryCustomerDetails(query_request)
        # return client.service.QueryCustomerDetails(query_request)

    def post_transaction_details(self, transaction_data):
        """
        make a transaction.
        transaction_data: dictionary with "PostFieldX":"PostFieldX_value",
        where X is a value 1,2,18,etc.
        Check pegpay documentation for PostField specifics.
        """
        # self.client = suds.client.Client(self.pegpay_url)
        if self.client is None:
            print ':Self.client is None'
            client_data = self.init_client()
            self.client = client_data
        else:
            print ':Self.cient not None'
        # client = self.init_client()

        # TransactionRequest instance
        transaction_request = self.client.factory.create('TransactionRequest')

        # transaction_request=client.factory.create('TransactionRequest')

        # iterate transaction_data dictionary, assign PostField values
        for postfield in transaction_data:
            transaction_request[postfield] = transaction_data[postfield]

        # post transaction,return response
        # return self.client.service.PostTransaction(transaction_request)


        # if transaction_data['PostField21'] == 'PREPAID':
        #     #
        #     return self.client.service.PrepaidVendorPostTransaction(transaction_request)
        # elif transaction_data['PostField21'] == 'POSTPAID':
        #     #
        #     return self.client.service.PostTransaction(transaction_request)

        # return client.service.PostTransaction(transaction_request)

        return self.client.service.PrepaidVendorPostTransaction(transaction_request)



    def paytv_bouquets(self, pay_tv, bouquet_code=None):
        """get pay tv Bouquets."""
        post_data = {}

        post_data['pay_tv'] = pay_tv
        post_data['bouquet_code'] = None

        if bouquet_code is not None:
            post_data['bouquet_code'] = bouquet_code

        try:
            data = query_tv_bouquets(post_data)
            #response_object = self.create_query(data, "ArrayOfBouquetDetails")
            response_object = self.create_query(data, "QueryRequest")
            print ':Response object: ',str(response_object)
            #response = response_map(response_object)
            print ':paytv_bouquets success'
            import json

        except Exception as e:
            print ':paytv_bouquets error: ', str(e)

    def track_transaction_status(self,vendorid,vendor=None,sender_id=None):
        """
        track transaction status, return result to
        seeker when success or fail.
        """
        print ':Testing tasks. Vendor ID = ',str(vendorid)
        transaction_response = None
        statuscode = None
        ussd_data = None
        response = {}
        status_caller = None

        try:
            result = self.TransactionDetails(vendorid)
            print '::Result ',str(result)
            statuscode = result.get('status_code', statuscode)
            statuscode = int(statuscode)

            if statuscode == 1000 or statuscode == 100  or statuscode == 0:
                print ':Status code is 1000'

                response['result'] = result
                result['vendor_id'] = vendorid

                if vendor == 'useremit':
                    print '::Track transaction. vendor useremit'
                    status_caller = Useremit()
                    status_caller.transaction_status(result,sender_id)
                    print ':Pre useremit data: ', str(result)
                elif vendor == 'remitussd':
                    status_caller = RemitUssd()
                    #status_caller.transaction_status(result)
                    status_caller.transaction_status(result,sender_id)
                    print ':Pre REmitUssd data: ', str(result)

                #remitussd = RemitUssd()

                #print ':Pre REmitUssd data: ', str(result)

                #remitussd.transaction_status(result)

        except Exception as e:
            print ':Track transaction error: ',str(e)





    def create_query(self, customer_data, request_method):
        """
        Create a pegpay Query.
        customer_data: dictionary containing QueryField and value.
        Supply dictionary with "QueryFieldX":"QueryFieldX_value" sets.
        where X is a value 1,2,18,etc.
        Check pegpay documentation for QueryField specifics.
        request_name: This is the factory request method.
        """

        # initiate client
        if self.client is None:
            client_data = self.init_client()
            self.client = client_data

        # create factory method
        query_request = self.client.factory.create(request_method)



        #query_request = self.client.factory.create("ArrayOfBouquetDetails")

        # Iterate customer_data dict, assign QueryField values
        for queryfield in customer_data:
            query_request[queryfield] = customer_data[queryfield]

        print 'query_request: ', str(query_request)

        return self.run_method(query_request, 1)

    def run_method(self, query_request, method_name):
        """
        Run pegasus method, return response.
        method_name digits:
        1.GetPayTVBouquetDetails
        """
        method_response = None

        if method_name == 1:
            try:
                method_response = self.client.service.GetPayTVBouquetDetails(query_request)
                print 'Method response success: ',str(method_response)
            except Exception as e:
                print 'Method response failed: ',str(e)

        return method_response




    def init_client(self):
        '''
        initiate and return client
        '''
        #print ':client init reached'
        try:
            #
            import urllib2
            import ssl
            ssl._create_default_https_context = ssl._create_unverified_context

        except Exception as e:
            print 'Client creation error: ', str(e)
        client = suds.client.Client(self.pegpay_url, timeout=800)
        # print ':Client: ',str(client)
        return client
