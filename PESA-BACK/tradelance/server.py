import remitapi.settings as settings
import requests
import xmltodict

class Tradelance():
    """
    Tradelance Api
    """

    def __init__(self):
        self.APIUsername = settings.TRADELANCE_USERNAME
        self.APIPassword = settings.TRADELANCE_PASSWORD
        self.APIEndpoint = settings.TRADELANCE_ENDPOINT
        self.APIKey = None

    def send_xml_request(self,xml):
        '''
        send xml
        '''
        headers = {
        'content_type':'application/xml'
        }

        response = None

        try:
            do_post = requests.post(self.APIEndpoint,data=xml,
            headers = headers,verify=False)

            data = xmltodict.parse(do_post.text)


            response = dict((k.lower(), v) for k, v in data.iteritems())

        except Exception as e:
            print 'xml error ',str(e)

        return response
