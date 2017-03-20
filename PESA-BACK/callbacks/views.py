from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
import remitapi.settings as settings
import xmltodict
import xml.etree.ElementTree as ET
from api import utils
from django.contrib.auth import authenticate, login
from pesapot_sms.server import Sms
from pegpay.models import UtilityTransaction

from useremit import  *





@csrf_exempt
def process_africas(request):
    try:
        print ':Callback entered'
        debug('callback entered', 'callback test', 'api')
        # admin_user = settings.ADMIN_USER
        # admin_key = settings.ADMIN_USER_KEY
        # user = authenticate(username=admin_user,password=admin_key)

        use = "eversend"


        if user is not None:
            debug('User not none', 'callback test', 'api')
            debug(str(request.method), 'callback request type', 'api')
            if request.method == 'POST':
                transaction_id = None
                referencenum = None
                names = None
                phonenumber = None
                paid_by = 'UseRemit'
                amount = None
                billtype = None
                message= 'paybill'
                account_type = None




                debug('callback request is post', 'africas_response error', 'api')
                post_values = request.body

                status = post_values['status']
                requestId = post_values['requestId']

                response_data = dict(post_values)

                print ':Response V: ',str(response_data)
                debug(str(response_data), 'callback response', 'api')
                status = str(response_data['Status']).lower()

                #print(response_data['Signature'])
               
                   
                    
                debug('id match', 'callback response', 'api')
                print 'transaction id',status

                  
        

            else:
                print 'NOt post'
                debug('callback not post', 'callback post values', 'api')

        else:
            debug('User is None', 'callback test', 'api')



    except Exception as e:
        'post error: ',str(e)









@csrf_exempt
def process_africas(request):
    try:
        print ':Callback entered'
        debug('callback entered', 'callback test', 'api')
        # admin_user = settings.ADMIN_USER
        # admin_key = settings.ADMIN_USER_KEY
        # user = authenticate(username=admin_user,password=admin_key)

        use = "eversend"


        if user is not None:
            debug('User not none', 'callback test', 'api')
            debug(str(request.method), 'callback request type', 'api')
            if request.method == 'POST':
                transaction_id = None
                referencenum = None
                names = None
                phonenumber = None
                paid_by = 'UseRemit'
                amount = None
                billtype = None
                message= 'paybill'
                account_type = None




                debug('callback request is post', 'africas_response error', 'api')
            

                status = post_values['status']
                requestId = post_values['requestId']

                response_data = dict(post_values)

                print ':Response V: ',str(response_data)
                debug(str(response_data), 'callback response', 'api')
                status = str(response_data['Status']).lower()

                #print(response_data['Signature'])
               
                   
                    
                debug('id match', 'callback response', 'api')
                print 'transaction id',status

                  
        

            else:
                print 'NOt post'
                debug('callback not post', 'callback post values', 'api')

        else:
            debug('User is None', 'callback test', 'api')



    except Exception as e:
        'post error: ',str(e)





@csrf_exempt
def process_beyonic(request):
    try:
        print ':Callback entered'
        debug('callback entered', 'callback test', 'api')
        admin_user = settings.ADMIN_USER
        admin_key = settings.ADMIN_USER_KEY
        user = authenticate(username=admin_user,password=admin_key)



        if user is not None:
            debug('User not none', 'callback test', 'api')
            debug(str(request.method), 'callback request type', 'api')
            if request.method == 'POST':
                transaction_id = None
                referencenum = None
                names = None
                phonenumber = None
                paid_by = 'UseRemit'
                amount = None
                billtype = None
                message= 'paybill'
                account_type = None




                debug('callback request is post', 'pegpay_response error', 'api')
                post_values = request.body

                dict_data = dict((k.lower(), v) for k, v in post_values.iteritems())

                response_data = dict_data['data']

                response_data = dict(response_data)

                print ':Response V: ',str(response_data)
                debug(str(response_data), 'callback response', 'api')
                status = str(response_data['Status']).lower()

                #print(response_data['Signature'])
                if response_data['status'] and status == 'successful':
                    debug('Status valid', 'callback response', 'api')
                    transaction_id = response_data['remote_transaction_id']
                   
                    
                    debug('id match', 'callback response', 'api')
                    print 'transaction id',str(transaction_id)

                  
        

            else:
                print 'NOt post'
                debug('callback not post', 'callback post values', 'api')

        else:
            debug('User is None', 'callback test', 'api')



    except Exception as e:
        'post error: ',str(e)


    return render_view(request, 'tlance.html',{})
    #return None












@csrf_exempt
def process_payment(request):
    null = None
    import json, ast

    try:
        print ':Callback entered'
        print "POST DATA", request.POST
        post_values = request.body
        post_values=json.loads(post_values)

        print "BODY DATA", post_values

        callback_response = post_values['result']

        print 'CALL BACK RESPONSE', callback_response

        vendor_id= callback_response['metadata']['transid']

        print 'VENDOR ID:', vendor_id

        transaction_state = callback_response['state']

        print "Transaction State:", transaction_state

        
        

        td = UtilityTransaction.objects.all()
        for td in td:
            print 'USEREMIT TRANS ID', td.beyon_transid
            if td.beyon_transid == vendor_id:
                print "Successfully returned transaction id:", td.beyon_transid
                callback_response = json.dumps(post_values['result'])
                call_post = {'callback_response':eval(callback_response),'vendor_id':vendor_id.encode('ascii'),'transaction_state':transaction_state.encode('ascii')} 
                print 'Call POST: ',call_post

                useremit = Useremit()
                # useremit.beyonic_trans_status(call_post)


        
        
            
               
                    
                
    
   
    except Exception as e:
        'post error: ',str(e)


          
    



@csrf_exempt
def process_payment2(request):
    null = None
    import json, ast

    try:
        print ':Callback entered'
        print "POST DATA", request.POST
        post_values = request.body
        callback_response=json.loads(post_values)

        print "BODY DATA", post_values

        print 'CALL BACK RESPONSE', callback_response

        vendor_id= callback_response['metadata']['transid']

        print 'VENDOR ID:', vendor_id

        transaction_state = callback_response['state']

        print "Transaction State:", transaction_state

        
        

        td = UtilityTransaction.objects.all()
        for td in td:
            print 'USEREMIT TRANS ID', td.beyon_transid
            if td.beyon_transid == vendor_id:
                print "Successfully returned transaction id:", td.beyon_transid
                callback_response = json.dumps(callback_response)
                call_post = {'callback_response':eval(callback_response),'vendor_id':vendor_id.encode('ascii'),'transaction_state':transaction_state.encode('ascii')} 
                print 'Call POST: ',call_post

                useremit = Useremit()
                # useremit.beyonic_trans_status(call_post)


        
        
            
               
                    
                
    
   
    except Exception as e:
        'post error: ',str(e)


          
    









