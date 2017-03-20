import sys
import suds
from suds import client
from suds.plugin import MessagePlugin
from suds.sax.element import Element
from suds.sax.attribute import Attribute
import remitapi.settings as settings
from remitapi.utils import debug
import requests
import hashlib
import time




class Smart():
    """Handle smart calls."""

    def __init__(self):
        self.smart_username = settings.SMART_USERNAME
        self.smart_password = settings.SMART_PASSWORD
        self.smart_endpoint = settings.SMART_ENDPOINT
        self.client = None

    def create_request(self, method_type, data):
        """make smart request."""
        #init client if not initiated
        print ':Create request'
        method_types={
            '1': 'spAirtimeTopup',
            '2': 'spBundlePurchase',
            '3': 'spCheckTransStatus',
            '4': 'spPayments',
            '5': 'spWithdrawDeposit'
        }


        if not self.client:
            self.client = self.init_client()

        request_method = method_types[method_type]

        query_request = self.client.factory.create(request_method)

        # add data to request
        # for queryfield in data:
        #     query_request[queryfield] = data[queryfield]



        try:
            request_method_type = int(method_type)
        except Exception as e:
            debug(e, 'smart method to int', 'smart')


        return self.run_request(query_request, request_method_type, data)

    def run_request(self, query_request, smart_method, data):
        """
        Run smart method, return response.
        method_name digits:
        1.spAirtimeTopup
        2.spBundlePurchase
        3.spCheckTransStatus
        4.spPayments
        5.spWithdrawDeposit
        """
        method_response = None

        try:
            if smart_method == 1:
                query_request['uuid'] = '3459874'
                query_request['username'] = self.smart_username
                query_request['password'] = self.smart_password
                query_request['subsmobileNo'] = '740065314'
                query_request['amount'] = '1000'

                print ':Query Request: ',str(query_request)
                method_response = self.client.service.spAirtimeTopup(query_request)
            elif smart_method == 2:
                method_response = self.client.service.spBundlePurchase(query_request)
            elif smart_method == 3:
                method_response = self.client.service.spCheckTransStatus(query_request)
            elif smart_method == 4:
                #{'uuid':'594480546844','subsmobileNo':'740065314','amount':'1000'}
                query_request['uuid'] = data['uuid']
                query_request['subsmobileNo'] = data['subsmobileNo']
                query_request['amount'] = data['amount']
                query_request['username'] = self.smart_username
                query_request['password'] = self.smart_password

                method_response = self.client.service.spPayments(query_request)
            elif smart_method == 5:
                method_response = self.client.service.spWithdrawDeposit(query_request)

        except Exception as e:
            debug(e, 'smart method error', 'smart')

        return method_response

    def init_client(self):
        """initiate smart client."""
        header = {'content-type': 'text/xml'}
        try:
            # import ssl
            # ssl._create_default_https_context = ssl._create_unverified_context
            self.client = suds.client.Client(self.smart_endpoint,headers=header,timeout=800)
            return self.client
        except Exception as e:
            debug(e, 'smart init client error', 'smart')
