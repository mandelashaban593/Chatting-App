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
from xml.etree import ElementTree as etree
from remitapi.models import App


class Smart():
    """Handle smart calls."""

    def __init__(self):
        self.smart_username = settings.SMART_USERNAME
        self.smart_password = settings.SMART_PASSWORD
        self.smart_endpoint = settings.SMART_ENDPOINT
        self.xml_top = """
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:smar="http://smartpesaapi.smart.ug/">
        <soapenv:Header/>
        <soapenv:Body>
        """
        self.xml_end = """
        </soapenv:Body>
         </soapenv:Envelope>
        """

        self.header = {'content-type': 'text/xml'}

        self.smart_methods = [
            'smar:spPayments',
            'smar:spCheckTransStatus',
            'smar:spWithdrawDeposit',
            'smar:spSendReceiveMoney',
            'smar:spAirtimeTopup',
        ]

    def smart_request(self, data, request, smart_method):
        "make smart requests"
        smart_method = int(smart_method)

        data['username'] = self.smart_username
        data['password'] = self.smart_password
        xml_data = None

        # generate uuid/ref_number
        if not data.get('uuid', ''):
            try:
                transaction = App()
                user = request.user
                amount = float(data['amount'])
                transaction.amount = amount
                transaction.owner = user
                transaction.save()
                data['uuid'] = str(transaction.transactionid)
                print ':transaction id: ', str(data['uuid'])
                print ':Database save successfull'
            except Exception as e:
                print ':Save database failed ', str(e)

        xml_data = self.generate_xml(self.smart_methods[smart_method], data)

        # if smart_method == 0 or smart_method == 1:
        #     xml_data = self.generate_xml(self.smart_methods[smart_method], data)
        # else:
        #     xml_data = self.manually_generate_xml(smart_method, data)

        response = self.make_request(xml_data)
        #print ':Full xml ', str(xml_data)
        #return 'blank'
        print '::Response ',str(response)

        return response

    def generate_xml(self, xml_element, data_dict):
        """
        generate required xml.basically works like this:
        root = etree.Element("element_name")
        etree.SubElement(root,'sub_element_name').text = 'sub_element_value'
        required_xml = etree.tostring(root)
        Unfortunately, smart cant get their shit together
        so some smart_methods have to do some of this manually and ruin this beauty of a method. bloody hell
        """

        xml_root = etree.Element(xml_element)

        for key, value in data_dict.iteritems():
            etree.SubElement(xml_root, key).text = value

        xml_data = etree.tostring(xml_root)



        full_xml = "%s%s%s" % (self.xml_top, xml_data, self.xml_end)
        print ':Full xml: ', full_xml
        return full_xml

    def manually_generate_xml(self, smart_method, data_dict):
        """
        manually generate xml, coz smart cudnt
        get their shit together.
        """
        full_xml = None
        user_data = ''

        credentials = "<username>%s</username><password>%s</password>" % (self.smart_username, self.smart_password)

        print ":Credentials ",str(credentials)


        for key, value in data_dict.iteritems():
            "<"+key+">"
            user_data = user_data + "<"+key+">" + value +"</"+key+">"
            #etree.SubElement(xml_root, key).text = value

        print ':user_data ',str(user_data)


        if smart_method == 2:
            xml_root = "<%s>" % (self.smart_methods[smart_method])
            xml_root_close = "</ns2:spWithdrawDeposit>"
            full_xml = "%s%s%s%s%s" % (self.xml_alternate_top, xml_root, user_data, xml_root_close, self.xml_alternate_end)

        print ':Full xml ',full_xml

        return full_xml


    def make_request(self, xml_data):
        response = None
        try:
            response = requests.post(self.smart_endpoint, data=xml_data, headers=self.header)
        except Exception as e:
            print ':Smart request error ', e
        return response.content
