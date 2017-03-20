''' ipay '''
import remitapi.settings as settings
import urllib
from remitapi.utils import debug
import requests


class Ipay():

    def __init__(self):
        self.settings = settings

    def check_source(self, request):
        source = True
        values_to_check = ['id', 'ivm', 'txncd']
        for x in values_to_check:
            if not x in request.GET:
                source = False
        return source

    def DepositMoney(self, transaction):
        """
        * Withdraw funds from Ipay account and add to a phone's Mobile Money account
        * @param float  amount The amount of money to deposit
        * @param string phone_number Phone number to pull Mobile Money from <br> [Format]: 254772123456
        * @param string narrative A description of the transaction 
        * @param string ref_text The text to be returned to the user's phone after the transaction is complete
        * 
        * ------------------------------------------------------------------------------------------------------------------
        *
        """

        # debug(transaction)
        url = 'https://www.ipayafrica.com/bulkpay/'
        params = {'live': settings.LIVE}
        amount = transaction.amount
        try:
            amount = round(float(amount))
        except Exception, e:
            print e
        try:
            amount = int(amount)
        except Exception, e:
            print e
        params['amt'] = amount
        params['tel'] = transaction.phonenumber
        params['vid'] = settings.IPAY_USER
        params['hid'] = self.ipay_hash(params)

        params = urllib.urlencode(params)
        bulkpay_link = "%s?%s" % (url, params)
        debug(bulkpay_link, 'bulkpay link', 'ipay')
        r = requests.get(bulkpay_link, verify=False)
        response = {}
        try:
            print r.text
            response = r.text
        except Exception, e:
            debug(e, 'error process ipay', 'mpesa')
            response['error'] = e
        return response

    def ipay_hash(self, p):
        import hmac
        import hashlib
        data = '%s%s%s' % (
            p['tel'],
            p['amt'],
            p['vid'])
        debug(data, 'hashdata', 'ipay')
        hash_key = hmac.new(settings.IPAY_HASH_KEY, data,
                            hashlib.sha1).hexdigest()
        return hash_key
