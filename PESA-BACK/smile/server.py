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
from remitapi.models import App,Smile_Session
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)   
import xmltodict
import json
import lxml.objectify
import datetime
from datetime import timedelta
from django.utils.timezone import utc



class Smile():
    """Handle smart calls."""

    def __init__(self):
        self.smile_username = settings.SMILE_USERNAME
        self.smile_password = settings.SMILE_PASSWORD
        self.smile_endpoint = settings.SMILE_ENDPOINT
        self.xml_top = """
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
		xmlns:tpgw="http://xml.smilecoms.com/schema/TPGW">
		<soapenv:Header/>
		<soapenv:Body>

        """
        self.xml_end = """
        </soapenv:Body>
		</soapenv:Envelope>

        """

        self.header = {'content-type': 'text/xml'}

        self.smile_methods = [
            'tpgw:Authenticate',
            'tpgw:BalanceQuery',
            'tpgw:BalanceTransfer',
            'tpgw:ValidateAccountQuery',
            'tpgw:BundleCatalogueQuery',
            'tpgw:BuyBundle',
            'tpgw:TransactionStatusQuery',
            'tpgw:NewCustomer',
            'tpgw:ValidateReferenceIdQuery',
            'tpgw:ValidateEmailAddressQuery',

           
        ]

    def smart_request(self, data, request, smile_method):
        "make smart requests"
        smile_method = int(smile_method)

        data['username'] = self.smile_username
        data['password'] = self.smile_password
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

        xml_data = self.generate_xml(self.smile_methods[smart_method], data)

        # if smart_method == 0 or smart_method == 1:
        #     xml_data = self.generate_xml(self.smart_methods[smart_method], data)
        # else:
        #     xml_data = self.manually_generate_xml(smart_method, data)

        response = self.make_request(xml_data)
        #print ':Full xml ', str(xml_data)
        #return 'blank'
        print '::Response ',str(response)

        return response

    def smile_auth_request(self, data, request, smile_method):
        "make smile requests"
        smile_method = 0
        

        data['Username'] = settings.SMILE_USERNAME
        data['Password'] = settings.SMILE_PASSWORD

        print "Username %s" % data['Username'] 
        print "Password %s" % data['Password'] 

        xml_data = None

        xml_data = self.generate_xml(self.smile_methods[smile_method], data)

        
        response = self.make_request(xml_data)
        #print ':Full xml ', str(xml_data)
        #return 'blank'
        print '::Response ',str(response)

        obj = lxml.objectify.fromstring(response)
        i = 0
        sess = ''

        for e in obj.iter():
            if i == 3:
                sess=str(e)
            i=i+1
            print "SESSION ID %s "  % sess

            request.session['SessionId'] = sess

        sess_date = datetime.datetime.utcnow().replace(tzinfo=utc)


        try:
            sess_stor = Smile_Session.objects.get(id=1)
            if not sess_stor:
                sess_stor = Smile_Session(session=sess,date_created = sess_date)
                sess_stor.save()
            else:
                print "Session Id", sess_stor.session

                sess_stor.session=sess
                print "SESSION ID 2 %s "  % sess_stor.session
                sess_stor.save()
        except Exception, e:
            print "Session Save Error", e
            sess_stor = Smile_Session(session=sess,date_created = sess_date)
            sess_stor.save()



        data = xmltodict.parse(response)

        response = dict((k.lower(), v) for k, v in data.iteritems())

        print '::Response 1 ',str(response)
        
        



        

    def smile_request(self, data, request, smile_method):
        "make smart requests"
        smile_method = int(smile_method)

        xml_data = None

        xml_data = self.generate_xml(self.smile_methods[smile_method], data)

        # if smart_method == 0 or smart_method == 1:
        #     xml_data = self.generate_xml(self.smart_methods[smart_method], data)
        # else:
        #     xml_data = self.manually_generate_xml(smart_method, data)

        response = self.make_request(xml_data)
        #print ':Full xml ', str(xml_data)
        #return 'blank'
        print '::Response ',str(response)

        return response

    def smile_request_cat(self, data, request, smile_method):
        "make smart requests"
        smile_method = int(smile_method)

        xml_data = None
        smile_data = {}

        smile_data = {}

        if 'SessionId' in request.session:
            SessionId=request.session['SessionId']
        else:
            self.smile_auth_request(smile_data, request, 0)
            SessionId=request.session['SessionId']
            

        trans_date = datetime.datetime.utcnow().replace(tzinfo=utc)
    

        sess_stor = None


        try:
            sess_stor = Smile_Session.objects.get(id=1)
        except Exception, e:
            self.smile_auth_request(smile_data, request, 0)
            print "Session was not found"

        sess_stor = Smile_Session.objects.get(id=1)



        
       
        self.smile_auth_request(smile_data, request, 0)
            


        SessionId=request.session['SessionId']
        print "SessionId Is 3 %s" % (SessionId)

        xml_data = """<S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/"><S:Body><BundleCatalogueQuery xmlns="http://xml.smilecoms.com/schema/TPGW"><TPGWContext><SessionId>%s</SessionId></TPGWContext></BundleCatalogueQuery></S:Body></S:Envelope>""" % (SessionId)
        # if smart_method == 0 or smart_method == 1:
        #     xml_data = self.generate_xml(self.smart_methods[smart_method], data)
        # else:
        #     xml_data = self.manually_generate_xml(smart_method, data)

        response = self.make_request(xml_data)
        #print ':Full xml ', str(xml_data)
        #return 'blank'
        print '::Response ',str(response)

        return response


    def smile_request_bal(self, data, request, smile_method):
        "make smart requests"
        smile_method = int(smile_method)

        xml_data = None

        smile_data = {}

        if 'SessionId' in request.session:
            SessionId=request.session['SessionId']
        else:
            self.smile_auth_request(smile_data, request, 0)
            SessionId=request.session['SessionId']

        print "SessionId Is %s" % (SessionId)
        AccountId=data['AccountId']

        xml_data = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tpgw="http://xml.smilecoms.com/schema/TPGW"><soapenv:Header/><soapenv:Body><tpgw:BalanceQuery><tpgw:TPGWContext><tpgw:SessionId>%s</tpgw:SessionId></tpgw:TPGWContext><tpgw:AccountId>%s</tpgw:AccountId></tpgw:BalanceQuery></soapenv:Body></soapenv:Envelope>""" % (SessionId, AccountId)
        # if smart_method == 0 or smart_method == 1:
        #     xml_data = self.generate_xml(self.smart_methods[smart_method], data)
        # else:
        #     xml_data = self.manually_generate_xml(smart_method, data)

        response = self.make_request(xml_data)
        #print ':Full xml ', str(xml_data)
        #return 'blank'
        print '::Response ',str(response)

        return response

    def smile_request_baltrans(self, data, request, smile_method):
        "make smart requests"
        smile_method = int(smile_method)

        xml_data = None

        smile_data = {}

        if 'SessionId' in request.session:
            SessionId=request.session['SessionId']
        else:
            self.smile_auth_request(smile_data, request, 0)
            SessionId=request.session['SessionId']

        print "SessionId Is %s" % (SessionId)

        FromAccountId=data['FromAccountId']
        ToAccountId=data['ToAccountId']
        TransferAmountInCents=data['TransferAmountInCents']
        UniqueTransactionId=data['UniqueTransactionId']

        xml_data = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tpgw="http://xml.smilecoms.com/schema/TPGW"><soapenv:Header/><soapenv:Body><tpgw:BalanceTransfer><tpgw:TPGWContext><tpgw:SessionId>%s</tpgw:SessionId></tpgw:TPGWContext><tpgw:FromAccountId>%s</tpgw:FromAccountId><tpgw:ToAccountId>%s</tpgw:ToAccountId><tpgw:TransferAmountInCents>%s</tpgw:TransferAmountInCents><tpgw:UniqueTransactionId>%s</tpgw:UniqueTransactionId></tpgw:BalanceTransfer></soapenv:Body></soapenv:Envelope>""" % (SessionId, FromAccountId, ToAccountId,TransferAmountInCents,UniqueTransactionId)
        # if smart_method == 0 or smart_method == 1:
        #     xml_data = self.generate_xml(self.smart_methods[smart_method], data)
        # else:
        #     xml_data = self.manually_generate_xml(smart_method, data)

        response = self.make_request(xml_data)
        #print ':Full xml ', str(xml_data)
        #return 'blank'
        print '::Response ',str(response)

        return response  


    def request_valacct(self, data, request, smile_method):
        "make smart requests"
        smile_method = int(smile_method)

        xml_data = None

        smile_data = {}

        if 'SessionId' in request.session:
            SessionId=request.session['SessionId']
        else:
            self.smile_auth_request(smile_data, request, 0)
            SessionId=request.session['SessionId']


        AccountId=data['AccountId']
        xml_data = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                    xmlns:tpgw="http://xml.smilecoms.com/schema/TPGW">
                    <soapenv:Header/>
                    <soapenv:Body>
                    <tpgw:ValidateAccountQuery>
                    <tpgw:TPGWContext>
                    <tpgw:SessionId>%s</tpgw:SessionId>
                    </tpgw:TPGWContext>
                    <tpgw:AccountId>%s</tpgw:AccountId>
                    </tpgw:ValidateAccountQuery>
                    </soapenv:Body>
                    </soapenv:Envelope>""" % (SessionId,AccountId)
        # if smart_method == 0 or smart_method == 1:
        #     xml_data = self.generate_xml(self.smart_methods[smart_method], data)
        # else:
        #     xml_data = self.manually_generate_xml(smart_method, data)

        response = self.make_request(xml_data)
        #print ':Full xml ', str(xml_data)
        #return 'blank'
        print '::Response ',str(response)

        return response



    def request_valacct(self, data, request, smile_method):
        "make smart requests"
        smile_method = int(smile_method)

        xml_data = None

        smile_data = {}

        if 'SessionId' in request.session:
            SessionId=request.session['SessionId']
        else:
            self.smile_auth_request(smile_data, request, 0)
            SessionId=request.session['SessionId']

        print "SessionId Is %s" % (SessionId)

        AccountId=data['AccountId']
        xml_data = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                    xmlns:tpgw="http://xml.smilecoms.com/schema/TPGW">
                    <soapenv:Header/>
                    <soapenv:Body>
                    <tpgw:ValidateAccountQuery>
                    <tpgw:TPGWContext>
                    <tpgw:SessionId>%s</tpgw:SessionId>
                    </tpgw:TPGWContext>
                    <tpgw:AccountId>%s</tpgw:AccountId>
                    </tpgw:ValidateAccountQuery>
                    </soapenv:Body>
                    </soapenv:Envelope>""" % (SessionId,AccountId)
        # if smart_method == 0 or smart_method == 1:
        #     xml_data = self.generate_xml(self.smart_methods[smart_method], data)
        # else:
        #     xml_data = self.manually_generate_xml(smart_method, data)

        response = self.make_request(xml_data)
        #print ':Full xml ', str(xml_data)
        #return 'blank'
        print '::Response ',str(response)

        return response
    def buybundle(self, data, request, smile_method):
        "make smart requests"
        smile_method = int(smile_method)

        xml_data = None
        smile_data = {}

        sess_stor = Smile_Session.objects.get(id=1)

        if 'SessionId' in request.session:
            SessionId=request.session['SessionId']
        else:
            self.smile_auth_request(smile_data, request, 0)
            SessionId=request.session['SessionId']

        print "SessionId Is %s" % (SessionId)

        BundleTypeCode=data['BundleTypeCode']
        CustomerAccountId=data['CustomerAccountId']
        QuantityBought=data['QuantityBought']
        CustomerTenderedAmountInCents=data['CustomerTenderedAmountInCents']
        UniqueTransactionId=data['UniqueTransactionId']
        
        

        xml_data = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tpgw="http://xml.smilecoms.com/schema/TPGW"><soapenv:Header/><soapenv:Body><tpgw:BuyBundle><tpgw:TPGWContext><tpgw:SessionId>%s</tpgw:SessionId></tpgw:TPGWContext><tpgw:BundleTypeCode>%s</tpgw:BundleTypeCode><tpgw:CustomerAccountId>%s</tpgw:CustomerAccountId><tpgw:CustomerTenderedAmountInCents>%s</tpgw:CustomerTenderedAmountInCents><tpgw:QuantityBought>%s</tpgw:QuantityBought><tpgw:UniqueTransactionId>%s</tpgw:UniqueTransactionId></tpgw:BuyBundle></soapenv:Body></soapenv:Envelope>""" % (SessionId,BundleTypeCode,CustomerAccountId,CustomerTenderedAmountInCents,QuantityBought,UniqueTransactionId)
        print xml_data
        # if smart_method == 0 or smart_method == 1:
        #     xml_data = self.generate_xml(self.smart_methods[smart_method], data)
        # else:
        #     xml_data = self.manually_generate_xml(smart_method, data)

        response = self.make_request(xml_data)
        #print ':Full xml ', str(xml_data)
        #return 'blank'
        print '::Response ',str(response)

        return response

    def trans_status(self, data, request, smile_method):
        "make smart requests"
        smile_method = int(smile_method)
        smile_data = {}

        xml_data = None

        sess_stor = Smile_Session.objects.get(id=1)

        if 'SessionId' in request.session:
            SessionId=request.session['SessionId']
        else:
            self.smile_auth_request(smile_data, request, 0)
            SessionId=request.session['SessionId']


        

        print "SessionId Is %s" % (SessionId)

        UniqueTransactionId=data['UniqueTransactionId']
        

        xml_data = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                         xmlns:tpgw="http://xml.smilecoms.com/schema/TPGW">
                        <soapenv:Header/>
                        <soapenv:Body>
                        <tpgw:TransactionStatusQuery>
                        <tpgw:TPGWContext>
                        <tpgw:SessionId>%s
                        </tpgw:SessionId>
                        </tpgw:TPGWContext>
                        <tpgw:UniqueTransactionId>%s</tpgw:UniqueTransactionId>
                        </tpgw:TransactionStatusQuery>
                        </soapenv:Body>
                        </soapenv:Envelope>""" % (SessionId,UniqueTransactionId)
        # if smart_method == 0 or smart_method == 1:
        #     xml_data = self.generate_xml(self.smart_methods[smart_method], data)
        # else:
        #     xml_data = self.manually_generate_xml(smart_method, data)
        print xml_data

        response = self.make_request(xml_data)
        #print ':Full xml ', str(xml_data)
        #return 'blank'
        print '::Response  of authentication',str(response)

        return response 



    def newcustomer(self, data, request, smile_method):
        "make smart requests"
        smile_method = int(smile_method)

        xml_data = None
        smile_data = {}

        sess_stor = Smile_Session.objects.get(id=1)

        if 'SessionId' in request.session:
            SessionId=request.session['SessionId']
        else:
            self.smile_auth_request(smile_data, request, 0)
            SessionId=request.session['SessionId']


        print "SessionId Is %s" % (SessionId)

        FirstName=data['FirstName']
        MiddleName=data['MiddleName']
        LastName=data['LastName']
        IdentityNumber=data['IdentityNumber']
        IdentityNumberType=data['IdentityNumberType']
        
        Line1=data['Line1']
        Line2=data['Line2']
        Zone=data['Zone']
        Town=data['Town']
        State=data['State']
        Country=data['Country']
        Code=data['Code']
        Type=data['Type']
        PostalMatchesPhysical=data['PostalMatchesPhysical']
        DateOfBirth=data['DateOfBirth']
        Gender=data['Gender']
        Language=data['Language']
        EmailAddress=data['EmailAddress']
        AlternativeContact1=data['AlternativeContact1']
        AlternativeContact2=data['AlternativeContact2']
        MothersMaidenName=data['MothersMaidenName']
        Nationality=data['Nationality']
        PassportExpiryDate=data['PassportExpiryDate']
        
        
        
        

        

        xml_data = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tpgw="http://xml.smilecoms.com/schema/TPGW"><soapenv:Header/><soapenv:Body><tpgw:NewCustomer><tpgw:TPGWContext><tpgw:SessionId>%s</tpgw:SessionId></tpgw:TPGWContext><tpgw:FirstName>%s</tpgw:FirstName><tpgw:MiddleName>%s</tpgw:MiddleName><tpgw:LastName>%s</tpgw:LastName><tpgw:IdentityNumber>%s</tpgw:IdentityNumber><tpgw:IdentityNumberType>%s</tpgw:IdentityNumberType><tpgw:Addresses><tpgw:Line1>%s</tpgw:Line1><tpgw:Line2>%s</tpgw:Line2><tpgw:Zone>%s</tpgw:Zone><tpgw:Town>%s</tpgw:Town><tpgw:State>%s</tpgw:State><tpgw:Country>%s</tpgw:Country><tpgw:Code>%s</tpgw:Code><tpgw:Type>%s</tpgw:Type><tpgw:PostalMatchesPhysical>%s</tpgw:PostalMatchesPhysical></tpgw:Addresses><tpgw:DateOfBirth>%s</tpgw:DateOfBirth><tpgw:Gender>%s</tpgw:Gender><tpgw:Language>%s</tpgw:Language><tpgw:EmailAddress>%s</tpgw:EmailAddress><tpgw:AlternativeContact1>%s</tpgw:AlternativeContact1><tpgw:AlternativeContact2>%s</tpgw:AlternativeContact2><tpgw:MothersMaidenName>%s</tpgw:MothersMaidenName><tpgw:Nationality>%s</tpgw:Nationality><tpgw:PassportExpiryDate>%s</tpgw:PassportExpiryDate></tpgw:NewCustomer></soapenv:Body></soapenv:Envelope>
                        """ % (SessionId,FirstName,MiddleName,LastName,IdentityNumber,IdentityNumberType,Line1,Line2,Zone,Town,State,Country,Code,Type,PostalMatchesPhysical,DateOfBirth,Gender,Language,EmailAddress,AlternativeContact1,AlternativeContact2,MothersMaidenName,Nationality,PassportExpiryDate  )
        # if smart_method == 0 or smart_method == 1:
        #     xml_data = self.generate_xml(self.smart_methods[smart_method], data)
        # else:
        #     xml_data = self.manually_generate_xml(smart_method, data)
        print xml_data
        
        response = self.make_request(xml_data)
        #print ':Full xml ', str(xml_data)
        #return 'blank'
        print '::Response ',str(response)

        return response 


    def valref(self, data, request, smile_method):
        "make smart requests"
        smile_method = int(smile_method)

        smile_data = {}

        xml_data = None

        sess_stor = Smile_Session.objects.get(id=1)

        if 'SessionId' in request.session:
            SessionId=request.session['SessionId']
        else:
            self.smile_auth_request(smile_data, request, 0)
            SessionId=request.session['SessionId']


        print "SessionId Is %s" % (SessionId)

        ReferenceId=data['ReferenceId']
        

        xml_data = """<soapenv:Envelope
                        xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                        xmlns:tpgw="http://xml.smilecoms.com/schema/TPGW">
                        <soapenv:Header/>
                        <soapenv:Body>
                        <tpgw:ValidateReferenceIdQuery>
                        <tpgw:TPGWContext>
                        <tpgw:SessionId>%s</tpgw:SessionId>
                        </tpgw:TPGWContext>
                        <tpgw:ReferenceId>%s</tpgw:ReferenceId>
                        </tpgw:ValidateReferenceIdQuery>
                        </soapenv:Body>
                        </soapenv:Envelope>""" % (SessionId,ReferenceId)
        # if smart_method == 0 or smart_method == 1:
        #     xml_data = self.generate_xml(self.smart_methods[smart_method], data)
        # else:
        #     xml_data = self.manually_generate_xml(smart_method, data)

        response = self.make_request(xml_data)
        #print ':Full xml ', str(xml_data)
        #return 'blank'
        print '::Response ',str(response)

        return response     



    def valemail(self, data, request, smile_method):
        "make smart requests"
        smile_method = int(smile_method)
        smile_data = {}

        xml_data = None

        sess_stor = Smile_Session.objects.get(id=1)

        if 'SessionId' in request.session:
            SessionId=request.session['SessionId']
        else:
            self.smile_auth_request(smile_data, request, 0)
            SessionId=request.session['SessionId']



        SessionId=request.session['SessionId']

        print "SessionId Is %s" % (SessionId)

        EmailAddress=data['EmailAddress']
        

        xml_data = """<soapenv:Envelope
                        xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                        xmlns:tpgw="http://xml.smilecoms.com/schema/TPGW">
                        <soapenv:Header/>
                        <soapenv:Body>
                        <tpgw:ValidateEmailAddressQuery>
                        <tpgw:TPGWContext>
                        <tpgw:SessionId>%s</tpgw:SessionId>
                        </tpgw:TPGWContext>
                        <tpgw:EmailAddress>%s</tpgw:EmailAddress>
                        </tpgw:ValidateEmailAddressQuery>
                        </soapenv:Body>
                        </soapenv:Envelope>""" % (SessionId,EmailAddress)
        # if smart_method == 0 or smart_method == 1:
        #     xml_data = self.generate_xml(self.smart_methods[smart_method], data)
        # else:
        #     xml_data = self.manually_generate_xml(smart_method, data)

        response = self.make_request(xml_data)
        #print ':Full xml ', str(xml_data)
        #return 'blank'
        print '::Response ',str(response)

        return response 



    def valephone(self, data, request, smile_method):
        "make smart requests"
        smile_method = int(smile_method)

        xml_data = None

        sess_stor = Smile_Session.objects.get(id=1)

        SessionId=request.session['SessionId']

        print "SessionId Is %s" % (SessionId)
        
        PhoneNumber=data['PhoneNumber']
        

        xml_data = """<soapenv:Envelope
                        xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                        xmlns:tpgw="http://xml.smilecoms.com/schema/TPGW">
                        <soapenv:Header/>
                        <soapenv:Body>
                        <tpgw:ValidatePhoneNumberQuery>
                        <tpgw:TPGWContext>
                        <tpgw:SessionId>%s</tpgw:SessionId>
                        </tpgw:TPGWContext>
                        <tpgw:PhoneNumber>%s</tpgw:PhoneNumber>
                        </tpgw:ValidatePhoneNumberQuery>
                        </soapenv:Body>
                        </soapenv:Envelope>""" % (SessionId,PhoneNumber)
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
            response = requests.Session().post(self.smile_endpoint, data=xml_data, headers=self.header, verify=False)
        except Exception as e:
            print ':Smile request error ', e
        return response.content
