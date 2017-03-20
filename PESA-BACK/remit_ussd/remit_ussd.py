
import remitapi.settings as settings
import requests
import json

class RemitUssd():
    """send transaction status to remit ussd."""

    def __init__(self):
        try:
            self.KEY = settings.USSDREMIT_KEY
            self.TOKEN = settings.USSDREMIT_TOKEN
            self.END_POINT = settings.USSDREMIT_TRANSACTIONSTATUS_URL
        except AttributeError:
            raise AttributeError(
                "Please add USSDREMIT_URL, USSDREMIT_TOKEN & USSDREMIT_KEY to your settings"
            )

    def conn(self, url, data={}, headers={}, method='POST'):
        """establish connection."""
        headers['Authorization'] = 'Token %s' % self.TOKEN

        req = requests.Request(
            method,
            url,
            headers=headers,
            data=data
        )

        prepared = req.prepare()
        self.pretty_print_POST(prepared)
        s = requests.Session()
        response = {}
        r = s.send(prepared, verify=False)

        if r.status_code == 200:
            print ':Connection established'
            response = r.text
        else:
            print ':Connection failed'

        return response

    def transaction_status(self, status_data,sender_id=None):
        url = self.END_POINT
        json_data = None
        json_string = None
        transaction_data = {}
        print ':URL: ',str(url)
        print '::STATUS DATA:',str(status_data)
        print '::Transaction status sender id: ',str(sender_id)

        try:

            json_string = json.dumps(status_data)
            #json_string = json.dumps(transaction_data)
            transaction_data['transaction_status'] = json_string
            #json_data = json.loads(status_data)
            if sender_id:
                transaction_data['ussd_id'] = sender_id

            #print '::JSON success ',str(json_string)
            print '::JSON success ',str(transaction_data)
        except Exception as e:
            print '::JSON failed ',str(e)

        #response = self.conn(url, status_data)
        #response = self.conn(url, json_string)
        response = self.conn(url, transaction_data)

    def pretty_print_POST(self, req):
        """
        At this point it is completely built and ready
        to be fired; it is "prepared".

        However pay attention at the formatting used in
        this function because it is programmed to be pretty
        printed and may differ from the actual request.
        """
        print('{}\n{}\n{}\n\n{}'.format(
            '-----------START-----------',
            req.method + ' ' + req.url,
            '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            req.body,
        ))
