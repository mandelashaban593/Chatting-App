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


class Rwanda():

    def __init__(self):
        self.settings = settings

    def DepositMoney(self, transaction):
        """
        * Withdraw funds from rwanda account and add to a phone's Mobile Money account
        * @param float  amount The amount of money to deposit
        * @param string phone_number Phone number to pull Mobile Money from <br> [Format]: 254772123456
        * @param string narrative A description of the transaction 
        * @param string ref_text The text to be returned to the user's phone after the transaction is complete
        *
        """

        url = settings.RWANDA_URL
        username = settings.RWANDA_USERNAME
        password = settings.RWANDA_PASSWORD
        params = {}
        params['amount'] = transaction.amount
        try:
            params['amount'] = round(float(transaction.amount))
        except Exception, e:
            debug(e, 'rwanda amount error', 'rwanda')

        amount = params['amount']
        mobilephone = transaction.phonenumber
        remitid = transaction.transactionid
        senderreason = transaction.senderreason
        sendername = transaction.sendername
        response = {}
        timestamp = int(time.time())
        import pytz
        from datetime import datetime
        timestamp=str(datetime.now(pytz.timezone('UTC')))
        cstr = "%s%s%s" % (username,password,timestamp)
        partnerpassword = hashlib.sha256(cstr).hexdigest()
        payload = { "mobilephone":"%s" % mobilephone, 
        "amount":"%s" % amount, 
 "senderreason":"%s" % senderreason, 
 "sendername":"%s" % sendername, 
 "remitid":"%s" % remitid, 
 "timestamp":"%s" % timestamp,
 "partnerpassword":"%s" % partnerpassword,
 "username":"%s" %username
}       
        debug(payload, 'processing rwanda payload', 'rwanda')
        try:
            r = requests.post(url, data=payload, auth=(
                username, password), verify=False,)
            response = r.text
        except Exception, e:
            debug(e, 'error processing rwanda', 'rwanda')
            response['error'] = e
        return response


    def QueryAccount(self, transaction):


        url = settings.RWANDA_URL
        params = {}
        params['mi_msgid'] = transaction['mi_msgid']
        params['mt_msgtype'] = transaction['mt_msgtype']
        mi_msgid=params['mi_msgid']
        mt_msgtype= params['mt_msgtype']
        
        in_rdparty= "esale-3rdparty-integrator"
        iv_version="1.2.0"
        mt_msgtype=mt_msgtype
        ak_apikey="useremit"
        as_apisecret="phbt54do7xqmx2"
        ar_accountref="00020000525986"
        di_deviceid="00020000525986-01"
        it_deviceidtype="DEVICE_UID"
        du_deviceuid="00020000525986-01"
        dt_devicetype="THIRD_PARTY_INTEGRATOR"
        ul_userLanguage="en"
        
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'user-agent':'eSale_Client/v1.2.0'}

        response = {}
       
        payload={"rq":{"in":in_rdparty,"iv":iv_version,"mt":mt_msgtype,"mi":mi_msgid,"ak":ak_apikey,"as":as_apisecret,"ar":ar_accountref,"di":di_deviceid,"it":it_deviceidtype,"du":du_deviceuid,"dt":dt_devicetype,"ul":ul_userLanguage,"rp":[{}]}}
        debug(payload, 'processing rwanda payload', 'rwanda')
        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers)
            response = r.text
        
        except Exception, e:
            debug(e, 'error processing rwanda', 'rwanda')
            response['error'] = e
        return response



        # partnerpassword = hashlib.sha256(cstr).hexdigest()
        # payload = { "in":"esale-3rdparty-integrator", 
        # "iv":"1.2.0", 
        # "mt":"CD02", 
        # "ak":"bkatm",
        # "as":"8cu5k13x3vjhng" ,
        # "ar":"00020000525986", 
        # "di":"00020000525986-01", 
        # "dt":"THIRD_PARTY_INTEGRATOR", 
        # "du":"00020000525986-01", 
        # "it":"DEVICE_UID", 
        # "ul":"UserLanguage",
        # }  


       
    def EnquirePayment(self, transaction):
      
        url = settings.RWANDA_URL
        params = {}
        params['mi_msgid'] = transaction['mi_msgid']
        params['productRef'] = transaction['productRef']
        params['consumerRef'] = transaction['consumerRef']
        params['mt_msgtype'] = transaction['mt_msgtype']
        params['amount'] = transaction['amount']
        mi_msgid=params['mi_msgid'] 
        productRef=params['productRef']
        consumerRef=params['consumerRef'] 
        mt_msgtype=params['mt_msgtype'] 
        amount=params['amount'] 

        in_rdparty= "esale-3rdparty-integrator"
        iv_version="1.2.0"
        mt_msgtype=mt_msgtype
        ak_apikey="useremit"
        as_apisecret="phbt54do7xqmx2"
        ar_accountref="00020000525986"
        di_deviceid="00020000525986-01"
        it_deviceidtype="DEVICE_UID"
        du_deviceuid="00020000525986-01"
        dt_devicetype="THIRD_PARTY_INTEGRATOR"
        ul_userLanguage="en"
        
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'user-agent':'eSale_Client/v1.2.0'}

        response = {}
       
        payload={"rq":{"in":in_rdparty,"iv":iv_version,"mt":mt_msgtype,"mi":mi_msgid,"ak":ak_apikey,"as":as_apisecret,"ar":ar_accountref,"di":di_deviceid,"it":it_deviceidtype,"du":du_deviceuid,"dt":dt_devicetype,"ul":ul_userLanguage,"rp":[{"p0":productRef,"p1":consumerRef,"p2":"","p3":amount}]}}
        debug(payload, 'processing rwanda payload', 'rwanda')
        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers)
            response = r.text
        except Exception, e:
            debug(e, 'error processing rwanda', 'rwanda')
            response['error'] = e
        return response



    def RetryPayment(self, transaction):
        
        url = settings.RWANDA_URL
        params = {}
        params['mi_msgid'] = transaction['mi_msgid']
        params['mt_msgtype'] = transaction['mt_msgtype']
        mi_msgid=params['mi_msgid']
        mt_msgtype= params['mt_msgtype']
        
        in_rdparty= "esale-3rdparty-integrator"
        iv_version="1.2.0"
        mt_msgtype=mt_msgtype
        ak_apikey="useremit"
        as_apisecret="phbt54do7xqmx2"
        ar_accountref="00020000525986"
        di_deviceid="00020000525986-01"
        it_deviceidtype="DEVICE_UID"
        du_deviceuid="00020000525986-01"
        dt_devicetype="THIRD_PARTY_INTEGRATOR"
        ul_userLanguage="en"
        
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'user-agent':'eSale_Client/v1.2.0'}

        response = {}
       
        payload={"rq":{"in":in_rdparty,"iv":iv_version,"mt":mt_msgtype,"mi":mi_msgid,"ak":ak_apikey,"as":as_apisecret,"ar":ar_accountref,"di":di_deviceid,"it":it_deviceidtype,"du":du_deviceuid,"dt":dt_devicetype,"ul":ul_userLanguage,"rp":[{"p0":mi_msgid}]}}
        debug(payload, 'processing rwanda payload', 'rwanda')
        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers)
            response = r.text
        except Exception, e:
            debug(e, 'error processing rwanda', 'rwanda')
            response['error'] = e
        return response



    def  GetTodayMiniReport(self, transaction):
        """
        * Withdraw funds from rwanda account and add to a phone's Mobile Money account
        * @param float  amount The amount of money to deposit
        * @param string phone_number Phone number to pull Mobile Money from <br> [Format]: 254772123456
        * @param string narrative A description of the transaction 
        * @param string ref_text The text to be returned to the user's phone after the transaction is complete
        *
        """

        url = settings.RWANDA_URL
        params = {}
        params['mt_msgtype'] = transaction['mt_msgtype']
        mt_msgtype= params['mt_msgtype']
        
        in_rdparty= "esale-3rdparty-integrator"
        iv_version="1.2.0"
        mt_msgtype=mt_msgtype
        ak_apikey="useremit"
        as_apisecret="phbt54do7xqmx2"
        ar_accountref="00020000525986"
        di_deviceid="00020000525986-01"
        it_deviceidtype="DEVICE_UID"
        du_deviceuid="00020000525986-01"
        dt_devicetype="THIRD_PARTY_INTEGRATOR"
        ul_userLanguage="en"
        
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'user-agent':'eSale_Client/v1.2.0'}

        response = {}
       
        payload={"rq":{"in":in_rdparty,"iv":iv_version,"mt":mt_msgtype,"mi":"","ak":ak_apikey,"as":as_apisecret,"ar":ar_accountref,"di":di_deviceid,"it":it_deviceidtype,"du":du_deviceuid,"dt":dt_devicetype,"ul":ul_userLanguage,"rp":[{}]}}
        debug(payload, 'processing rwanda payload', 'rwanda')
        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers)
            response = r.text
        except Exception, e:
            debug(e, 'error processing rwanda', 'rwanda')
            response['error'] = e
        return response

    def  GetDailyMiniReport(self, transaction):
        """
        * Withdraw funds from rwanda account and add to a phone's Mobile Money account
        * @param float  amount The amount of money to deposit
        * @param string phone_number Phone number to pull Mobile Money from <br> [Format]: 254772123456
        * @param string narrative A description of the transaction 
        * @param string ref_text The text to be returned to the user's phone after the transaction is complete
        *
        """

        url = settings.RWANDA_URL
        params = {}
        params['mt_msgtype'] = transaction['mt_msgtype']
        params['day'] = transaction['day']
        mt_msgtype= params['mt_msgtype']
        day= params['day']
        
        in_rdparty= "esale-3rdparty-integrator"
        iv_version="1.2.0"
        mt_msgtype=mt_msgtype
        ak_apikey="useremit"
        as_apisecret="phbt54do7xqmx2"
        ar_accountref="00020000525986"
        di_deviceid="00020000525986-01"
        it_deviceidtype="DEVICE_UID"
        du_deviceuid="00020000525986-01"
        dt_devicetype="THIRD_PARTY_INTEGRATOR"
        ul_userLanguage="en"
        
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'user-agent':'eSale_Client/v1.2.0'}

        response = {}
       
        payload={"rq":{"in":in_rdparty,"iv":iv_version,"mt":mt_msgtype,"mi":"","ak":ak_apikey,"as":as_apisecret,"ar":ar_accountref,"di":di_deviceid,"it":it_deviceidtype,"du":du_deviceuid,"dt":dt_devicetype,"ul":ul_userLanguage,"rp":[{"p0":day}]}}
        debug(payload, 'processing rwanda payload', 'rwanda')
        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers)
            response = r.text
        except Exception, e:
            debug(e, 'error processing rwanda', 'rwanda')
            response['error'] = e
        return response



    def PaymentMiniHistoryPerProduct(self, transaction):
        """
        * Withdraw funds from rwanda account and add to a phone's Mobile Money account
        * @param float  amount The amount of money to deposit
        * @param string phone_number Phone number to pull Mobile Money from <br> [Format]: 254772123456
        * @param string narrative A description of the transaction 
        * @param string ref_text The text to be returned to the user's phone after the transaction is complete
        *
        """

        url = settings.RWANDA_URL
        username = settings.RWANDA_USERNAME
        password = settings.RWANDA_PASSWORD
        params = {}
        params['messageId'] = transaction['messageId']
        params['userLanguage'] = transaction['userLanguage']
        params['offset'] = transaction['offset']
        params['maxNoItems'] = transaction['maxNoItems']
        params['product'] = transaction['product']
       

        messageId = params['messageId']
        userLanguage=  params['userLanguage']
        offset = params['offset']
        maxNoItems=  params['maxNoItems']
        product= params['product']
      

        response = {}
        timestamp = int(time.time())
        import pytz
        from datetime import datetime
        timestamp=str(datetime.now(pytz.timezone('UTC')))
        cstr = "%s%s%s" % (username,password,timestamp)
        partnerpassword = hashlib.sha256(cstr).hexdigest()
        payload = { "messageId":"%s" % messageId, 
        "userLanguage":"%s" % userLanguage, 
 "authSecret":"%s" % partnerpassword,
 "authKey":"%s" % username,
 "offset":"%s" % offset,
 "maxNoItems":"%s" %  maxNoItems,
 "product":"%s" % product,
}       
        debug(payload, 'processing rwanda payload', 'rwanda')
        try:
            r = requests.post(url, data=payload, auth=(
                username, password), verify=False,)
            response = r.text
        except Exception, e:
            debug(e, 'error processing rwanda', 'rwanda')
            response['error'] = e
        return response





    def ReissuePayment(self, transaction):
        """
        * Withdraw funds from rwanda account and add to a phone's Mobile Money account
        * @param float  amount The amount of money to deposit
        * @param string phone_number Phone number to pull Mobile Money from <br> [Format]: 254772123456
        * @param string narrative A description of the transaction 
        * @param string ref_text The text to be returned to the user's phone after the transaction is complete
        *
        """

        url = settings.RWANDA_URL
        params = {}
        params['mt_msgtype'] = transaction['mt_msgtype']
        params['receiptRef'] = transaction['receiptRef']
        mt_msgtype= params['mt_msgtype']
        receiptRef=params['receiptRef']
        
        in_rdparty= "esale-3rdparty-integrator"
        iv_version="1.2.0"
        mt_msgtype=mt_msgtype
        ak_apikey="useremit"
        as_apisecret="phbt54do7xqmx2"
        ar_accountref="00020000525986"
        di_deviceid="00020000525986-01"
        it_deviceidtype="DEVICE_UID"
        du_deviceuid="00020000525986-01"
        dt_devicetype="THIRD_PARTY_INTEGRATOR"
        ul_userLanguage="en"
        
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'user-agent':'eSale_Client/v1.2.0'}

        response = {}
       
        payload={"rq":{"in":in_rdparty,"iv":iv_version,"mt":mt_msgtype,"mi":"","ak":ak_apikey,"as":as_apisecret,"ar":ar_accountref,"di":di_deviceid,"it":it_deviceidtype,"du":du_deviceuid,"dt":dt_devicetype,"ul":ul_userLanguage,"rp":[{"p0":mt_msgtype, "p1":receiptRef}]}}
        debug(payload, 'processing rwanda payload', 'rwanda')
        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers)
            response = r.text
        except Exception, e:
            debug(e, 'error processing rwanda', 'rwanda')
            response['error'] = e
        return response



    def GetMonthlyMiniReport(self, transaction):
        """
        * Withdraw funds from rwanda account and add to a phone's Mobile Money account
        * @param float  amount The amount of money to deposit
        * @param string phone_number Phone number to pull Mobile Money from <br> [Format]: 254772123456
        * @param string narrative A description of the transaction 
        * @param string ref_text The text to be returned to the user's phone after the transaction is complete
        *
        """

        url = settings.RWANDA_URL
        params = {}
        params['mt_msgtype'] = transaction['mt_msgtype']
        mt_msgtype= params['mt_msgtype']
        
        in_rdparty= "esale-3rdparty-integrator"
        iv_version="1.2.0"
        mt_msgtype=mt_msgtype
        ak_apikey="useremit"
        as_apisecret="phbt54do7xqmx2"
        ar_accountref="00020000525986"
        di_deviceid="00020000525986-01"
        it_deviceidtype="DEVICE_UID"
        du_deviceuid="00020000525986-01"
        dt_devicetype="THIRD_PARTY_INTEGRATOR"
        ul_userLanguage="en"
        
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'user-agent':'eSale_Client/v1.2.0'}

        response = {}
       
        payload={"rq":{"in":in_rdparty,"iv":iv_version,"mt":mt_msgtype,"mi":"","ak":ak_apikey,"as":as_apisecret,"ar":ar_accountref,"di":di_deviceid,"it":it_deviceidtype,"du":du_deviceuid,"dt":dt_devicetype,"ul":ul_userLanguage,"rp":[{}]}}
        debug(payload, 'processing rwanda payload', 'rwanda')
        try:
            r = requests.post(url, data=json.dumps(payload), headers=headers)
            response = r.text
        except Exception, e:
            debug(e, 'error processing rwanda', 'rwanda')
            response['error'] = e
        return response