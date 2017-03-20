''' ipay '''
import remitapi.settings as settings
from remitapi.utils import debug
import requests
import hashlib
import time
import json
from django.utils import timezone 
from suds.client import Client

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Impal():

    def __init__(self):
        self.settings = settings

    def RequestDemo(self, transaction):
        """
        * Withdraw funds from rwanda account and add to a phone's Mobile Money account
        * @param float  amount The amount of money to deposit
        * @param string phone_number Phone number to pull Mobile Money from <br> [Format]: 254772123456
        * @param string narrative A description of the transaction 
        * @param string ref_text The text to be returned to the user's phone after the transaction is complete
        *
        """

        endpoint = settings.IMPAL_URL
        url = 'sessionid'
        url = "%s%s" % (
            endpoint,
            url
        )
        params = {}
        params['api_username'] = transaction.api_username
        params['api_password'] = transaction.api_password
		
        api_password=params['api_password']
        api_username = params['api_username']
        payload = { "api_username":"%s" % api_username, 
					 "api_password":"%s" % api_password, 
					}  
		
        debug(payload, 'processing impal payload', 'impal')
       	headers = {'Content-Type':'application/json', 'Accept':'application/json'}

        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers)
            response = r.text
        except Exception, e:
            debug(e, 'error processing impal', 'impal')
            response['error'] = e
        return response

    def ReqSesid(self, transaction):
        """
        * Withdraw funds from rwanda account and add to a phone's Mobile Money account
        * @param float  amount The amount of money to deposit
        * @param string phone_number Phone number to pull Mobile Money from <br> [Format]: 254772123456
        * @param string narrative A description of the transaction 
        * @param string ref_text The text to be returned to the user's phone after the transaction is complete
        *
        """
        endpoint = settings.IMPAL_URL
        url = ':portnumber/specialsessionid'
        url = "%s%s" % (
            endpoint,
            url
        )
        params = {}
        params['api_username'] = transaction.api_username
        params['api_password'] = transaction.api_password
   		 
        api_password=params['api_password']
        api_username=params['api_username']
        payload = { "api_username":"%s" % api_username, 
					 "api_password":"%s" % api_password, 
					}  
		
        debug(payload, 'processing impal payload', 'impal')
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
     
        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers)
            response = r.text
        except Exception, e:
            debug(e, 'error processing impal', 'impal')
            response['error'] = e
        return response

    def mnoTransfer(self, transaction):
        """
        * Withdraw funds from rwanda account and add to a phone's Mobile Money account
        * @param float  amount The amount of money to deposit
        * @param string phone_number Phone number to pull Mobile Money from <br> [Format]: 254772123456
        * @param string narrative A description of the transaction 
        * @param string ref_text The text to be returned to the user's phone after the transaction is complete
        *
        """

        endpoint = settings.IMPAL_URL
        url = 'mnoTransfer'
        url = "%s%s" % (
            endpoint,
            url
        )
        username = settings.IMPAL_USERNAME
        params = {}

        params['api_username'] = username
        params['session_id'] = transaction.session_id
        params['source_country_code'] = transaction.source_country_code
        params['sendername'] = transaction.sendername
        params['recipient_mobile'] = transaction.recipient_mobile
        params['amount'] = transaction.amount
        params['recipient_currency_code'] = transaction.recipient_currency_code
        params['recipient_country_code'] = transaction.recipient_country_code
        params['reference_number'] = transaction.reference_number
        params['sendertoken'] = transaction.sendertoken
        client_datetime = datetime.now(timezone.utc).isoformat()
        params['client_datetime'] = transaction.client_datetime

        api_username=params['api_username'] 
        session_id=params['session_id']
        source_country_code=params['source_country_code'] 
        sendername=params['sendername'] 
        recipient_mobile=params['recipient_mobile']
        amount=params['amount'] 
        recipient_currency_code=params['recipient_currency_code']
        recipient_country_code=params['recipient_country_code'] 
        reference_number=params['reference_number'] 
        sendertoken=params['sendertoken']
        client_datetime=params['client_datetime']  
        payload = { "api_username":"%s" % api_username, 
					 "session_id":"%s" % session_id,
					 "source_country_code":"%s" % source_country_code, 
					 "sendername":"%s" % sendername, 
					 "recipient_mobile":"%s" % recipient_mobile, 
					 "amount":"%s" % amount, 
					 "recipient_currency_code":"%s" % recipient_currency_code, 
					 "recipient_country_code":"%s" % recipient_country_code, 
					 "reference_number":"%s" % reference_number, 
					 "sendertoken":"%s" % sendertoken, 
					 "client_datetime":"%s" % client_datetime, 
					 
					}  
		
        debug(payload, 'processing impal payload', 'impal')
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
     
        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers)
            response = r.text
        except Exception, e:
            debug(e, 'error processing impal', 'impal')
            response['error'] = e
        return response



    def BankTransfer(self, transaction):
        """
        * Withdraw funds from rwanda account and add to a phone's Mobile Money account
        * @param float  amount The amount of money to deposit
        * @param string phone_number Phone number to pull Mobile Money from <br> [Format]: 254772123456
        * @param string narrative A description of the transaction 
        * @param string ref_text The text to be returned to the user's phone after the transaction is complete
        *
        """

        endpoint = settings.IMPAL_URL
        url = 'bankTransfer'
        url = "%s%s" % (
            endpoint,
            url
        )
        username = settings.IMPAL_USERNAME
        params = {}

        params['api_username'] = username
        params['session_id'] = transaction.session_id
        params['source_country_code'] = transaction.source_country_code
        params['sendername'] = transaction.sendername
        params['recipient_mobile'] = transaction.recipient_mobile
        params['recipient_currency_code'] = transaction.recipient_currency_code
        params['recipient_country_code'] = transaction.recipient_country_code
        params['reference_number'] = transaction.reference_number
        params['bank_code'] = transaction.bank_code
        client_datetime = datetime.now(timezone.utc).isoformat()
        params['client_datetime'] = transaction.client_datetime
        params['sender_city'] = transaction.sender_city
        params['sender_address'] = transaction.sender_address
        params['recipientname'] = transaction.recipientname
        params['accountnumber'] = transaction.accountnumber
  
        api_username=params['api_username'] 
        session_id=params['session_id']
        source_country_code=params['source_country_code'] 
        sendername=params['sendername'] 
        recipient_mobile=params['recipient_mobile']
        recipient_currency_code=params['recipient_currency_code']
        recipient_country_code=params['recipient_country_code'] 
        reference_number=params['reference_number'] 
        bank_code=params['bank_code'] 
        amount=params['amount']
        client_datetime=params['client_datetime'] 
        sender_address=params['sender_address'] 
        sender_city=params['sender_city']
        recipientname=params['recipientname']
        accountnumber=params['accountnumber']  

 
        payload = { "api_username":"%s" % api_username, 
					 "session_id":"%s" % session_id,
					 "source_country_code":"%s" % source_country_code, 
					 "sendername":"%s" % sendername, 
					 "recipient_mobile":"%s" % recipient_mobile,
					 "recipient_currency_code":"%s" % recipient_currency_code, 
					 "recipient_country_code":"%s" % recipient_country_code, 
					 "reference_number":"%s" % reference_number,  
					 "bank_code":"%s" % bank_code, 
					 "amount":"%s" % amount, 
					 "client_datetime":"%s" % client_datetime,
					 "sender_address":"%s" % sender_address,  
					 "sender_city":"%s" % sender_city, 
					 "recipientname":"%s" % recipientname, 
					 "accountnumber":"%s" % accountnumber, 
					  
					 
					}  

		
        debug(payload, 'processing impal payload', 'impal')
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
     
        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers)
            response = r.text
        except Exception, e:
            debug(e, 'error processing impal', 'impal')
            response['error'] = e
        return response


    def Balance(self, transaction):
        """
        * Withdraw funds from rwanda account and add to a phone's Mobile Money account
        * @param float  amount The amount of money to deposit
        * @param string phone_number Phone number to pull Mobile Money from <br> [Format]: 254772123456
        * @param string narrative A description of the transaction 
        * @param string ref_text The text to be returned to the user's phone after the transaction is complete
        *
        """
        endpoint = settings.IMPAL_URL
        url = 'balance'
        url = "%s%s" % (
            endpoint,
            url
        )
        username = settings.IMPAL_USERNAME
        params = {}

        params['api_username'] = username
        params['session_id'] = transaction.session_id
      
        
        api_username=params['api_username'] 
        session_id=params['session_id']
        
        payload = { "api_username":"%s" % api_username, 
					 "session_id":"%s" % session_id,
					 
					}  

		
        debug(payload, 'processing impal payload', 'impal')
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
     
        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers)
            response = r.text
        except Exception, e:
            debug(e, 'error processing impal', 'impal')
            response['error'] = e
        return response


    def TranStaus(self, transaction):
        """
        * Withdraw funds from rwanda account and add to a phone's Mobile Money account
        * @param float  amount The amount of money to deposit
        * @param string phone_number Phone number to pull Mobile Money from <br> [Format]: 254772123456
        * @param string narrative A description of the transaction 
        * @param string ref_text The text to be returned to the user's phone after the transaction is complete
        *
        """

        endpoint = settings.IMPAL_URL
        url = 'refNumStatus'
        url = "%s%s" % (
            endpoint,
            url
        )
        username = settings.IMPAL_USERNAME
        params = {}

        params['api_username'] = username
        params['reference_number'] = transaction.reference_number
      
        
        api_username=params['api_username'] 
        reference_number=params['reference_number']
        
        payload = { "api_username":"%s" % api_username, 
					 "reference_number":"%s" % reference_number,
					 
					}  

		
     
        debug(payload, 'processing impal payload', 'impal')
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers)
            response = r.text
        except Exception, e:
            debug(e, 'error processing impal', 'impal')
            response['error'] = e
        return response

	def XRate(self, transaction):
   
		endpoint = settings.IMPAL_URL
        url = 'xchangeRate'
        url = "%s%s" % (
            endpoint,
            url
        )
        username = settings.IMPAL_USERNAME
        params = {}

        params['api_username'] = username
        params['session_id'] = transaction.session_id
      	params['fromct'] = transaction.fromct
        params['to'] = transaction.to
      
     
        api_username=params['api_username'] 
        session_id=params['session_id']
        fromct=params['fromct'] 
        to=params['to']
        
        payload = { "api_username":"%s" % api_username, 
					 "session_id":"%s" % session_id,
					 "from":"%s" % fromct, 
					 "to":"%s" % to,
					 
					}  

		
        debug(payload, 'processing impal payload', 'impal')
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
     
        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers)
            response = r.text
        except Exception, e:
            debug(e, 'error processing impal', 'impal')
            response['error'] = e
        return response


    def verifybeneficiary(self, transaction):
        """
        * Withdraw funds from rwanda account and add to a phone's Mobile Money account
        * @param float  amount The amount of money to deposit
        * @param string phone_number Phone number to pull Mobile Money from <br> [Format]: 254772123456
        * @param string narrative A description of the transaction 
        * @param string ref_text The text to be returned to the user's phone after the transaction is complete
        *
        """

        endpoint = settings.IMPAL_URL
        url = 'verifybeneficiary'
        url = "%s%s" % (
            endpoint,
            url
        )
        username = settings.IMPAL_USERNAME
        params = {}

        params['api_username'] = username
        params['session_id'] = transaction.session_id
      	params['first_name'] = transaction.first_name
        params['second_name'] = transaction.second_name
        params['last_name'] = transaction.last_name
      	params['mobile_number'] = transaction.mobile_number
        params['country_code'] = transaction.country_code

        api_username=params['api_username'] 
        session_id=params['session_id']
        first_name=params['first_name'] 
        second_name=params['second_name']
        last_name=params['last_name']
        mobile_number=params['mobile_number'] 
        country_code=params['country_code']
        
        
        payload = { "api_username":"%s" % api_username, 
					 "session_id":"%s" % session_id,
					 "first_name":"%s" % first_name, 
					 "second_name":"%s" % second_name,
					 "last_name":"%s" % last_name,
					 "mobile_number":"%s" % mobile_number, 
					 "country_code":"%s" % country_code,
					 
					}  

		
     
        debug(payload, 'processing impal payload', 'impal')
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers)
            response = r.text
        except Exception, e:
            debug(e, 'error processing impal', 'impal')
            response['error'] = e
        return response


    def msisdnbalance(self, transaction):
        """
        * Withdraw funds from rwanda account and add to a phone's Mobile Money account
        * @param float  amount The amount of money to deposit
        * @param string phone_number Phone number to pull Mobile Money from <br> [Format]: 254772123456
        * @param string narrative A description of the transaction 
        * @param string ref_text The text to be returned to the user's phone after the transaction is complete
        *
        """

        endpoint = settings.IMPAL_URL
        url = 'msisdnbalance'
        url = "%s%s" % (
            endpoint,
            url
        )
        username = settings.IMPAL_USERNAME
        params = {}

        params['api_username'] = username
        params['session_id'] = transaction.session_id
        params['country_code'] = transaction.country_code

        api_username=params['api_username'] 
        session_id=params['session_id'] 
        country_code=params['country_code']
        
        
        payload = { "api_username":"%s" % api_username, 
					 "session_id":"%s" % session_id,
					 "country_code":"%s" % country_code,
					 
					}  

		
        debug(payload, 'processing impal payload', 'impal')
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
     
        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers)
            response = r.text
        except Exception, e:
            debug(e, 'error processing impal', 'impal')
            response['error'] = e
        return response





        



        