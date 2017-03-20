"""
Created by Muwa Isaac. muwaisaac@gmail.com
"""

import sys
import suds
from suds import client
from suds.plugin import MessagePlugin
from suds.sax.element import Element
from suds.sax.attribute import Attribute
import pegpay.utils
import remitapi.settings as settings
from datetime import datetime
import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)


class pegpay():

    """
    Handle payments for PegPay.
    Powered by suds [pip install suds]
    refference: https://fedorahosted.org/suds/wiki/Documentation
    """

    def __init__(self):
        self.pegpay_username = settings.PEGPAY_USERNAME
        self.pegpay_password = settings.PEGPAY_PASSWORD
        self.pegpay_url = settings.PEGPAY_URL
        #self.client = suds.client.Client(self.pegpay_url)
        self.client = None

    def query_customer_details(self,customer_data):
        """
        Check that customer is valid.
        customer_data: dictionary containing QueryField and value.
        Supply dictionary with "QueryFieldX":"QueryFieldX_value" sets.
        where X is a value 1,2,18,etc.
        Check pegpay documentation for QueryField specifics.
        """
        #self.client = suds.client.Client(self.pegpay_url)

        # create QueryRequest instance
        if self.client is None:
            print ':Self.client is None'
            client_data = self.init_client()
            self.client = client_data
        else:
            print ':Self.client not None'

        #client = self.init_client()
        query_request = self.client.factory.create('QueryRequest')
        #query_request = client.factory.create('QueryRequest')
        print ':Query Request: ',str(query_request)

        # Iterate customer_data dictionary,asighn QueryField values
        for queryfield in customer_data:
            query_request[queryfield]=customer_data[queryfield]

        # query customer details and return response
        return self.client.service.QueryCustomerDetails(query_request)
        #return client.service.QueryCustomerDetails(query_request)

    def post_transaction_details(self,transaction_data):
        """
        make a transaction.
        transaction_data: dictionary with "PostFieldX":"PostFieldX_value",
        where X is a value 1,2,18,etc.
        Check pegpay documentation for PostField specifics.
        """
        #self.client = suds.client.Client(self.pegpay_url)
        if self.client is None:
            print ':Self.client is None'
            client_data = self.init_client()
            self.client = client_data
        else:
            print ':Self.cient not None'
        #client = self.init_client()

        # TransactionRequest instance
        transaction_request=self.client.factory.create('TransactionRequest')

        #transaction_request=client.factory.create('TransactionRequest')

        #iterate transaction_data dictionary, assign PostField values
        for postfield in transaction_data:
            transaction_request[postfield]=transaction_data[postfield]

        # post transaction,return response
        return self.client.service.PostTransaction(transaction_request)
        #return client.service.PostTransaction(transaction_request)

    def get_transaction_details(self,transaction_data):
        """
        get posted transaction details
        """
        # TransactionRequest instance
        transaction_request=self.client.factory.create('GetTransactionDetails')

        #print 'Get Transaction request: ',str(transaction_request)
        #return transaction_request

        for postfield in transaction_data:
            #
            transaction_request[postfield]=transaction_data[postfield]

        try:
            return self.client.service.GetTransactionDetails(transaction_request)
        except Exception as e:
            raise





    def init_client(self):
        '''
        initiate and return client
        '''
        print ':client init reached'
        try:
            #
            import urllib2
            import ssl
            ssl._create_default_https_context = ssl._create_unverified_context

        except Exception as e:
            print 'Client creation error: ',str(e)
        client = suds.client.Client(self.pegpay_url,timeout=300)
            #print ':Client: ',str(client)
        return client
