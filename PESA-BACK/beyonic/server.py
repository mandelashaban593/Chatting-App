''' ipay '''
import remitapi.settings as settings
from remitapi.utils import debug
import requests
import hashlib
import time
import json
from suds.client import Client

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Beyonic():

    def __init__(self):
        self.settings = settings

   	

    def BeyonicCollectionRequests(self, transaction):
      
        url = settings.Beyonic_Callback_URL
        
        params = {}
        params['phonenumber'] = transaction['phonenumber']
        params['currency'] = transaction['currency']
        params['amount'] = transaction['amount']
        params['my_id'] = transaction['my_id']
        
        phonenumber=params['phonenumber'] 
        currency=params['currency']
        amount=params['amount'] 
        my_id=params['my_id']
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': 'Token 25c3c127128814646bfbcf44ee33a727845de6ca'}

        response = {}
       
        payload={"phonenumber":phonenumber,"currency":currency,"amount":amount,"metadata.my_id":my_id,"send_instructions":True}
        debug(payload, 'processing beyonic payload', 'beyonic')
        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers)
            response = r.text
        except Exception, e:
            debug(e, 'error processing beyonic', 'beyonic')
            response['error'] = e
        return response






       
    def BeyonicPayments(self, transaction):
      
        url = settings.Beyonic_URL
        callback_url = settings.Beyonic_Callback_URL2
        params = {}
        params['phonenumber'] = transaction['phonenumber']
        params['currency'] = transaction['currency']
        params['account'] = transaction['account']
        params['amount'] = transaction['amount']
        params['description'] = transaction['description']
        params['payment_type'] = transaction['payment_type']

        phonenumber=params['phonenumber'] 
        currency=params['currency']
        account=params['account'] 
        amount=params['amount'] 
        description=params['description'] 
        payment_type=params['payment_type'] 
        transid  = None

        

        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': 'Token 25c3c127128814646bfbcf44ee33a727845de6ca'}

        response = {}
       
        if '1' in transaction.values():
                transid = transaction['transid']
                payload={"phonenumber":phonenumber,"currency":currency,"account":account,"amount":amount,"description":description,"payment_type":payment_type,'callback_url':callback_url, 'metadata':{'transid':transid} }
        else:
            payload={"phonenumber":phonenumber,"currency":currency,"account":account,"amount":amount,"description":description,"payment_type":payment_type,'callback_url':callback_url}

        
        debug(payload, 'processing beyonic payload', 'beyonic')
        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers)
            response = r.text
        except Exception, e:
            debug(e, 'error processing beyonic', 'beyonic')
            response['error'] = e
        return response
