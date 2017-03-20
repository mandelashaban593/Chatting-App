try:
    from hashlib import sha1 as sha_constructor, md5 as md5_constructor
except ImportError:
    from django.utils.hashcompat import sha_constructor, md5_constructor
import random
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
import base64
from django.template import RequestContext

import sys
import os
import datetime
from datetime import datetime

from django.conf import settings

import M2Crypto
from M2Crypto import RSA, BIO
from M2Crypto import EVP
from base64 import b64encode, b64decode
import hashlib
import binascii

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.Hash import SHA
from Crypto.Hash import MD5

peg_user = settings.PEGPAY_USERNAME
peg_pass = settings.PEGPAY_PASSWORD

private_key_dir = os.path.dirname(__file__)
relative_path = "server.key.no_passphrase"
absolute_file_path = os.path.join(private_key_dir, relative_path)


def query_account_data(post_data):
    '''
    get post values, assign them to pegpay parameters and return "pegpay_parameter:post_value" dictionary.
    QueryField2,QueryField5 etc are pegpay specific parameters. Check pegpay docs for their details.
    '''
    post_values = post_data.copy()
    query_customer = {}
    if post_values['company_code'] == "NWSC" or post_values['company_code'] == "DSTV" or post_values['company_code'] == "GOTV":
        query_customer["QueryField2"] = post_values['area']

    query_customer["QueryField1"] = post_values['customer_ref']
    query_customer["QueryField4"] = post_values['company_code']
    query_customer["QueryField5"] = settings.PEGPAY_USERNAME
    query_customer["QueryField6"] = settings.PEGPAY_PASSWORD

    return query_customer

def query_tv_bouquets(post_data):
    """
    get post values, assign them to pegpay parameters and return "pegpay_parameter:post_value" dictionary.
    QueryField2,QueryField5 etc are pegpay specific parameters. Check pegpay docs for their details.
    """
    post_values = post_data.copy()
    query_bouquets = {}
    query_bouquets["QueryField1"] = ""

    try:
        if post_values['bouquet_code'] is not None:
            query_bouquets["QueryField1"] = post_values['bouquet_code']

        query_bouquets["QueryField4"] = post_values['pay_tv']
        query_bouquets["QueryField5"] = settings.PEGPAY_USERNAME
        query_bouquets["QueryField6"] = settings.PEGPAY_PASSWORD

        print 'utils query_tv_bouquets success'
    except Exception as e:
        print 'utils query_tv_bouquets error: ', str(e)

    return query_bouquets


def transaction_data(api_values):
    '''
    get post values, assign them to pegpay parameters and return "pegpay_parameter:post_value" dictionary.
    PostField17,PostField12 etc are pegpay specific parameters. Check pegpay docs for their details.
    '''
    post_data = api_values.copy()

    #transaction_ref = random_string_generator(12)
    transaction_ref = post_data.get('transactionid', ' ')
    # get current date
    todate = date_creator("/")
    transaction_data = {}

    pre_sign_list = []

    # get initial data
    customer_name = post_data.get('customer_name', ' ')
    sender_message = post_data.get('sender_message', 'Remit Bill Payment')
    customer_phone = post_data.get('customer_phone', ' ')
    paid_by = post_data.get('paid_by', ' ')
    customer_ref = post_data.get('customer_ref', '')
    amount = post_data.get('amount', '')
    company_code = post_data.get('company_code', '')
    area = post_data.get('area', '')
    paymethod = post_data.get('paymethod', '')

    print ':Transaction data: ',str(area)

    try:
        pre_sign_list = [
            customer_ref,
            customer_name,
            customer_phone,
            transaction_ref,
            settings.PEGPAY_USERNAME,
            settings.PEGPAY_PASSWORD,
            todate,
            paid_by,
            amount,
            sender_message,
            settings.PEGPAY_PAYMENT_TYPE
        ]
    except Exception, e:
        print "Pegpay pre sign Error : %s" % e

    private_key = absolute_file_path
    payment_type = settings.PEGPAY_PAYMENT_TYPE

    """
    print 'Private Path: ',str(private_key)
    """

    # umeme payment type
    umeme_payment_type = {
        'energypayment': '2',
        'reconnectionfee': '5',
        'inspectionfee': '14',
        'securitydeposit': '1',
        'capitalcontribution': '4',
        'bouncedchequefine': '3',
        'rechargeableworksorder': '6',
        'metertestfee': '7',
        'finegeneral': '9',
        'nonrefundtenderdeposit': '10'
    }

    string_to_sign = concat_string("", pre_sign_list)

    """
    print 'String to sign: ',str(string_to_sign)
    """

    signed_data = private_sign(private_key, string_to_sign)

    """
    print 'Signed Data: ',str(signed_data)
    """

    if company_code == "NWSC":

        transaction_data['PostField3'] = area
        print ':Company is water ',str(transaction_data['PostField3'])

    if company_code == "UMEME":
        transaction_data['PostField21'] = paymethod
        transaction_data['PostField6'] = '2'

    transaction_data['PostField17'] = settings.PEGPAY_CHEQUE_NUMBER
    transaction_data['PostField18'] = sender_message.replace(" ", "")
    transaction_data['PostField1'] = customer_ref
    transaction_data['PostField2'] = customer_name
    transaction_data['PostField11'] = customer_phone
    transaction_data['PostField20'] = transaction_ref
    transaction_data['PostField8'] = settings.PEGPAY_PAYMENT_TYPE
    transaction_data['PostField9'] = settings.PEGPAY_USERNAME
    transaction_data['PostField10'] = settings.PEGPAY_PASSWORD
    transaction_data['PostField14'] = paid_by
    transaction_data['PostField12'] = "0"
    transaction_data['PostField13'] = "1"
    transaction_data['PostField15'] = "0"
    transaction_data['PostField5'] = todate
    transaction_data['PostField7'] = amount
    transaction_data['PostField16'] = signed_data
    transaction_data['PostField19'] = post_data.get('customer_email', ' ')
    transaction_data['PostField4'] = company_code

    return transaction_data


def random_string_generator(string_len):
    """
    generate random string with length "string_len"
    """
    import string
    import random

    random_string = ''.join(random.choice(string.ascii_uppercase)
                            for i in range(string_len))
    return random_string


def date_creator(format):
    """
    return date with specified Format
    e.g "/","-",etc
    """
    current_date = datetime.today().date()
    todate = current_date.strftime('%d/%m/%Y')
    return todate

def send_date(currentdate):
    """
    return date with specified Format
    e.g "/","-",etc
    """
    #current_date = datetime.today().date()
    todate = currentdate.strftime('%d/%m/%Y')
    return todate


def private_sign(private_key_loc, data_string):


    try:
        key = open(private_key_loc, "r").read()
        rsakey = RSA.importKey(key)
        signer = PKCS1_v1_5.new(rsakey)
        sha_data = MD5.new(data_string).digest()
        new_signer = rsakey.sign(sha_data, '')
        digest = SHA.new()
        digest.update(data_string)
        sign = signer.sign(digest)
        #print 'Private key sign passed: ',str(sign)
    except Exception as e:
        print str(e)




    return b64encode(sign)


def concat_string(separator, string_object):
    """
    concatenate strings within a list or dictionary values(string_object)
    using specified separator("*","/","," etc)
    """
    concatenated_string = None

    if type(string_object) is list:
        concatenated_string = separator.join(
            str(item) for item in string_object).replace(" ", "")
    elif type(string_object) is dict:
        concatenated_string = separator.join(
            str(item) for item in string_object.values()).replace(" ", "")

    return concatenated_string


def get_transaction_data(api_values):
    post_data = api_values.copy()
    transaction_data = {}

    #print 'Get Transaction Ref Id: ',str(api_values.get('referenceid', ''))

    transaction_data['QueryField5'] = settings.PEGPAY_USERNAME
    transaction_data['QueryField6'] = settings.PEGPAY_PASSWORD
    transaction_data['QueryField10'] = api_values.get('referenceid', '')

    return transaction_data



def response_map(response_object):
    '''add descriptions to response codes'''
    response_data = response_object.__dict__
    mapped_data = None
    data_map = {
        "ResponseField1": "customer_reference",
        "ResponseField2": "customer_name",
        "ResponseField3": "area_tin",
        "ResponseField4": "oustanding_balance",
        "ResponseField5": "customer_type",
        "ResponseField6": "status_code",
        "ResponseField7": "status_description",
        "ResponseField8": "pegpay_tran_id",
        "ResponseField9": "company_payment_reference"
    }

    for item, val in response_data.items():
        try:
            #
            if data_map[item] is not None:
                response_data[data_map[item]] = response_data.pop(item)
            else:
                pass
                #print 'pop unsuccessful'

        except KeyError:
            #print ':Key Error...'
            del response_data[item]
            continue
        except Exception as e:
            print str(e)

    mapped_data = response_data

    if mapped_data is not None:
        return mapped_data
    else:
        return None

def obj_dict(obj):
    import json
    return obj.__dict__
