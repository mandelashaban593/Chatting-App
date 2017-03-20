'''
serializers for API
'''
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _


class DepositMoneySerializer(serializers.Serializer):
    amount = serializers.CharField()
    msisdn = serializers.CharField()

    def validate(self, attrs):
        amount = attrs.get('amount')
        msisdn = attrs.get('msisdn')
        if not msisdn or not amount:
            msg = _('You Must include "amount" and "msisdn".')
            raise serializers.ValidationError(msg)
        """
        if amount and msisdn:
            '''proceed with the translation'''
            balance = 0
            if amount > balance:
                msg = _(
                    'Account balance is too low, you neeed a minimum of %s.'
                % balance
                )
                raise serializers.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "amount" and "msisdn".')
            raise serializers.ValidationError(msg)
        """
        return attrs


class PaybillSerializer(serializers.Serializer):

    amount = serializers.CharField()
    referencenum = serializers.CharField()
    phonenumber = serializers.CharField()
    names = serializers.CharField()
    message = serializers.CharField()
    billtype = serializers.CharField()
    paymethod = serializers.CharField()
    #vendorid = None
    #vendor_id =serializers.CharField()
    vendor_id = None


    def validate(self, attrs):
        amount = attrs.get('amount')
        referencenum = attrs.get('referencenum')
        phonenumber = attrs.get('phonenumber')
        billtype = attrs.get('billtype')
        paymethod = attrs.get('paymethod')
        #vendor_id = attrs.get('vendor_id')


        if not referencenum or not amount or not phonenumber or not billtype:
            msg = (
                'You Must include "amount", "referencenum", "billtype" and "phonenumber" '
                )
            raise serializers.ValidationError(msg)

        return attrs

class PaybillWithAreaSerializer(serializers.Serializer):
    """
    Serializer for bill inclusize of area or tin
    """
    area = serializers.CharField()
    amount = serializers.CharField()
    referencenum = serializers.CharField()
    phonenumber = serializers.CharField()
    names = serializers.CharField()
    message = serializers.CharField()
    billtype = serializers.CharField()
    paymethod = serializers.CharField()
    vendorid = None

    def validate(self,attrs):
        #
        amount = attrs.get('amount')
        referencenum = attrs.get('referencenum')
        phonenumber = attrs.get('phonenumber')
        billtype = attrs.get('billtype')
        paymethod = attrs.get('paymethod')
        area = serializers.CharField()

        if not referencenum or not amount or not phonenumber or not billtype:
            msg = (
                'You Must include "amount", "referencenum", "billtype" and "phonenumber" '
                )
            raise serializers.ValidationError(msg)

        if billtype == "2" and area == None:
            msg = ('You must include "area"')
            raise serializers.ValidationError(msg)
        return attrs

class PaybillQueryAccountSerializer(serializers.Serializer):
    referencenum = serializers.CharField()
    location = serializers.CharField()
    billtype = serializers.CharField()

    def validate(self, attrs):
        referencenum = attrs.get('referencenum')
        billtype = attrs.get('billtype')
        if not referencenum or not billtype:
            msg = (
                'You Must include "referencenum" and "billtype" '
                )
            raise serializers.ValidationError(msg)
        return attrs

class PaybillTransactionDetailsSerializer(serializers.Serializer):
    vendorid = serializers.CharField()

    def validate(selft,attrs):

        vendorid = attrs.get('vendorid')

        return attrs

class TransactionStatusSerializer(serializers.Serializer):
    transaction_id = serializers.CharField()
    #transaction_type = serializers.CharField()

    def validate(self,attrs):
        transaction_id = attrs.get('transaction_id')

        #transaction_type = attrs.get('transaction_type')

        if not transaction_id:
            msg = _('You Must include "transaction_id"')
            raise
            serializers.ValidationError(msg)

        return attrs

class TradelanceDepositSerializer(serializers.Serializer):

    #username = serializers.CharField()
    #key = serializers.CharField()
    #timestamp = serializers.CharField()
    #api = serializers.CharField()
    receiver_number = serializers.CharField()
    amount = serializers.CharField()
    #refference = serializers.CharField()

    def validate(self,attrs):
        #username = attrs.get('username')
        #key = attrs.get('key')
        #timestamp = attrs.get('timestamp')
        #api = attrs.get('api')
        receiver_number = attrs.get('receiver_number')
        amount = attrs.get('amount')
        #refference = attrs.get('refference')

        if not receiver_number or not amount:
            msg = (
                'you must include "receiver_number","amount" and "refference"'
            )
            raise serializers.ValidationError(msg)

        return attrs

class TradelanceSerializer(serializers.Serializer):
    receiver_number = serializers.CharField()
    amount = serializers.CharField()

    def validate(self,attrs):
        receiver_number = attrs.get('receiver_number')
        amount = attrs.get('amount')
        if not receiver_number or not amount:
            msg = (
                'you must include "receiver_number","amount" and "refference"'
            )
            raise serializers.ValidationError(msg)

        return attrs

class TradelanceStatusSerializer(serializers.Serializer):

    transaction_id = serializers.CharField()

    def validate(self,attrs):
        transaction_id = attrs.get('transaction_id')

        if not transaction_id:
            msg = ('You must include "transaction_id"')
            raise serializers.ValidationError(msg)

        return attrs

class TradelanceStatementSerializer(serializers.Serializer):
    account = serializers.CharField()
    startdate = serializers.CharField()
    enddate = serializers.CharField()

    def validate(self,attrs):
        account = attrs.get('account')
        startdate = attrs.get('startdate')
        enddate = attrs.get('enddate')

        if not account or not startdate or not enddate:
            msg = (
            'you must include "account","startdate[yyyyMMddHHmmss]","enddate[yyyyMMddHHmmss]"'
            )

            raise serializers.ValidationError(msg)

        return attrs

class TradelanceTransferSerializer(serializers.Serializer):
    '''
    Transfer funds to a subscribers mobile account
    '''
    benificiary = serializers.CharField()
    amount = serializers.CharField()

    def validate(self,attrs):
        benificiary = attrs.get('benificiary')
        amount = attrs.get('amount')

        if not benificiary or not amount:
            msg = ('you must include "benificiary","amount"')

            raise serializers.ValidationError(msg)

        return attrs

class PaybillQueryTvBouquetSerializer(serializers.Serializer):
    """query pay tv Bouquets."""
    pay_tv = serializers.CharField()
    print 'the serializer'

    def validate(self, attrs):
        pay_tv = attrs.get('pay_tv')

        print ':paytv value ',str(pay_tv)

        if not pay_tv:
            msg = ('you must include "pay_tv"')

            raise serializers.ValidationError(msg)

        return attrs

class SmartGuardianSerializer(serializers.Serializer):
    """smart guardian data."""
    smart_data = serializers.CharField()

    def validaet(self, attrs):
        smart_data = attrs.get('smart_data')

        if not smart_data:
            msg = ('you must include "smart_data" and "slay"')

            raise serializers.ValidationError(msg)

        return attrs

class SmartPaymentsSerializer(serializers.Serializer):
    """smart spPayments serializer."""
    number = serializers.CharField()
    amount = serializers.CharField()

    def validate(self, attrs):
        number = attrs.get('number')
        amount = attrs.get('amount')

        if not number or not amount:
            raise serializers.ValidationError()
        return attrs

class SmartTransStatusSerializer(serializers.Serializer):
    """smart spCheckTransStatus serializer."""
    transaction_id = serializers.CharField()

    def validate(self, attrs):
        transaction_id = attrs.get('transaction_id')

        if not transaction_id:
            raise serializers.ValidationError()
        return attrs

class SmartWithdrawDepositSerializer(serializers.Serializer):
    """smart spWithdrawDeposit."""
    requesttype = serializers.CharField()
    number = serializers.CharField()
    amount = serializers.CharField()

    def validate(self, attrs):
        requesttype = attrs.get('requesttype')
        number = attrs.get('number')
        amount = attrs.get('amount')

        if not requesttype or not number or not amount:
            raise serializers.ValidationError()
        return attrs

class SmartSendReceiveMoneySerializer(serializers.Serializer):
    """smart spSendReceiveMoney."""
    number = serializers.CharField()
    amount = serializers.CharField()

    def validate(self, attrs):
        number = attrs.get('number')
        amount = attrs.get('amount')

        if not number or not amount:
            raise serializers.ValidationError()
        return attrs

class SmartAirtimeTopupSerializer(serializers.Serializer):
    """smart spAirtimeTopup."""
    sender_number = serializers.CharField()
    reciever_number = serializers.CharField()
    amount = serializers.CharField()

    def validate(self, attrs):
        sender_number = attrs.get('sender_number')
        reciever_number = attrs.get('reciever_number')
        amount = attrs.get('amount')

        if not sender_number or not reciever_number or not amount:
            raise serializers.ValidationError()

        return attrs

class ResidentClientSmsSerializer(serializers.Serializer):
    """client sms."""
    to = serializers.CharField()
    sms_message = serializers.CharField()
    sms_agent = serializers.CharField()
    sms_client = serializers.CharField()

    def validate(self,attrs):
        to = attrs.get('to')
        sms_message = attrs.get('sms_message')
        sms_agent = attrs.get('sms_agent')
        sms_client = attrs.get('sms_client')

        if not to or not sms_message or not sms_agent or not sms_client:
            raise serializers.ValidationError()

        return attrs


class ClientSmsSerializer(serializers.Serializer):
    """client sms."""
    to = serializers.CharField()
    sms_message = serializers.CharField()
    sms_client = serializers.CharField()

    def validate(self, attrs):
        to = attrs.get('to')
        sms_message = attrs.get('sms_message')
        sms_client = attrs.get('sms_client')

        if not to or not sms_message or not sms_client:
            raise serializers.ValidationError()

        return attrs

class RegisterNotifsClientSerializer(serializers.Serializer):
    """register notif client."""
    client_name = serializers.CharField()
    client_key = serializers.CharField()

    def validate(self,attrs):
        client_name = attrs.get('client_name')
        client_key = attrs.get('client_key')

        if not client_name or not client_key:
            raise serializers.ValidationError()

        return attrs

class SendMobileNotifSerializer(serializers.Serializer):
    """push notification serializer."""
    message_title = serializers.CharField()
    message_body = serializers.CharField()
    reg_id = serializers.CharField()
    client_id = serializers.CharField()

    def validate(self,attrs):
        message_title = attrs.get('message_title')
        message_body = attrs.get('message_body')
        reg_id = attrs.get('reg_id')
        client_id = attrs.get('client_id')

        if not message_title or not message_body or not reg_id or not client_id:
            raise serializers.ValidationError()

        return attrs


class RwandaQueryAccountSerializer(serializers.Serializer):
    """smart spPayments serializer."""
    mt_msgtype = serializers.CharField()
    def validate(self, attrs):

        mt_msgtype = attrs.get('mt_msgtype')

        if not mt_msgtype:
            raise serializers.ValidationError()
        return attrs





class RwandaEnquirePaymentSerializer(serializers.Serializer):
    """smart spPayments serializer."""

    productRef = serializers.CharField()
    consumerRef = serializers.CharField()
    mt_msgtype = serializers.CharField()
    amount   = serializers.CharField()



class RwandaRetryPaymentSerializer(serializers.Serializer):
    """smart spPayments serializer."""
    mi_msgid = serializers.CharField()
    mt_msgtype = serializers.CharField()
    def validate(self, attrs):

        mi_msgid = attrs.get('mi_msgid')
        mt_msgtype = attrs.get('mt_msgtype')

        if not mi_msgid or not mt_msgtype:
            raise serializers.ValidationError()
        return attrs


class RwandaReissuePaymentSerializer(serializers.Serializer):
    """smart spPayments serializer."""
    mt_msgtype = serializers.CharField()
    receiptRef = serializers.CharField()

    def validate(self, attrs):
        mt_msgtype = attrs.get('mt_msgtype')
        receiptRef = attrs.get('receiptRef')
        if not mt_msgtype or not receiptRef:
            raise serializers.ValidationError()
        return attrs

class RwandaPaymentMiniHistoryPerProductSerializer(serializers.Serializer):
    """smart spPayments serializer."""
    messageId = serializers.CharField()
    userLanguage = serializers.CharField()
    offset = serializers.CharField()
    maxNoItems = serializers.CharField()
    productRef  = serializers.CharField()
    def validate(self, attrs):
        messageId = attrs.get('messageId')
        userLanguage = attrs.get('userLanguage')
        offset = attrs.get('offset')
        maxNoItems = attrs.get('maxNoItems')
        productRef = attrs.get('productRef')
        if not messageId or not userLanguage or not offset or not  maxNoItems or not productRef:
            raise serializers.ValidationError()
        return attrs

class RwandaGetTodayMiniReportSerializer(serializers.Serializer):
    """smart spPayments serializer."""
    mt_msgtype = serializers.CharField()
    def validate(self, attrs):
        mt_msgtype = attrs.get('mt_msgtype')
        if not mt_msgtype:
            raise serializers.ValidationError()
        return attrs

class RwandaGetDailyMiniReportSerializer(serializers.Serializer):
    """smart spPayments serializer."""
    mt_msgtype = serializers.CharField()
    day = serializers.CharField()
    def validate(self, attrs):
        mt_msgtype = attrs.get('mt_msgtype')
        day = attrs.get('day')
        if not mt_msgtype:
            raise serializers.ValidationError()
        return attrs


class RwandaGetThisMonthMiniReportSerializer(serializers.Serializer):
    """smart spPayments serializer."""
    mt_msgtype = serializers.CharField()
    def validate(self, attrs):
        mt_msgtype = attrs.get('mt_msgtype')
        if not mt_msgtype:
            raise serializers.ValidationError()
        return attrs

class SmileAuthenticateSerializer(serializers.Serializer):
    """smart spPayments serializer."""
    Username = serializers.CharField()
    Password = serializers.CharField()
    def validate(self, attrs):
        Username = attrs.get('Username')
        Password = attrs.get('Password')
        if not Username or not Password:
            raise serializers.ValidationError()
        return attrs


class SmileBalanceQuerySerializer(serializers.Serializer):
    """smart spPayments serializer."""
    AccountId = serializers.CharField()



class SmileBalanceTransferSerializer(serializers.Serializer):
    """smart spPayments serializer."""
    ToAccountId = serializers.CharField()
    TransferAmountInCents = serializers.CharField()
    def validate(self, attrs):
        
        ToAccountId = attrs.get('ToAccountId')
        TransferAmountInCents = attrs.get('TransferAmountInCents')
        if  not ToAccountId or not TransferAmountInCents:
            raise serializers.ValidationError()
        return attrs

class SmileValidateAccountQuerySerializer(serializers.Serializer):
    """smart spPayments serializer."""
    
    AccountId = serializers.CharField()
    def validate(self, attrs):
        
        AccountId = attrs.get('AccountId')
        if not AccountId:
            raise serializers.ValidationError()
        return attrs






class SmileBuyBundleSerializer(serializers.Serializer):
    """smart spPayments serializer."""
    BundleTypeCode = serializers.CharField()
    CustomerAccountId = serializers.CharField()
    QuantityBought = serializers.CharField()
    CustomerTenderedAmountInCents = serializers.CharField()
    def validate(self, attrs):

        BundleTypeCode = attrs.get('BundleTypeCode')
        CustomerAccountId = attrs.get('CustomerAccountId')
        QuantityBought = attrs.get('QuantityBought')
        CustomerTenderedAmountInCents = attrs.get('CustomerTenderedAmountInCents')
        if not BundleTypeCode or not CustomerAccountId or not QuantityBought or not CustomerTenderedAmountInCents:
            raise serializers.ValidationError()
        return attrs


class SmileTransactionStatusQuerySerializer(serializers.Serializer):
    """smart spPayments serializer."""
    UniqueTransactionId = serializers.CharField()

    def validate(self, attrs):
        UniqueTransactionId = attrs.get('UniqueTransactionId')
        if not UniqueTransactionId:
            raise serializers.ValidationError()
        return attrs

class SmileNewCustomerSerializer(serializers.Serializer):
    """smart spPayments serializer."""
   
    FirstName = serializers.CharField()
    MiddleName = serializers.CharField()
    LastName = serializers.CharField()
    IdentityNumber = serializers.CharField()
    IdentityNumberType = serializers.CharField()
    Line1 = serializers.CharField()
    Line2 = serializers.CharField()
    Zone = serializers.CharField()
    Town = serializers.CharField()
    State = serializers.CharField()
    Country = serializers.CharField()
    Code = serializers.CharField()
    Type = serializers.CharField()
    PostalMatchesPhysical = serializers.CharField()
    DateOfBirth = serializers.CharField()
    Gender = serializers.CharField()
    Language = serializers.CharField()
    EmailAddress= serializers.CharField()
    AlternativeContact1= serializers.CharField()
    AlternativeContact2= serializers.CharField()
    MothersMaidenName = serializers.CharField()
    Nationality = serializers.CharField()
    PassportExpiryDate = serializers.CharField()
    def validate(self, attrs):
       
        FirstName = attrs.get('FirstName')
        if  not FirstName:
            raise serializers.ValidationError()
        return attrs




class SmileValidateReferenceIdSerializer(serializers.Serializer):
    """smart spPayments serializer."""
    ReferenceId = serializers.CharField()

    def validate(self, attrs):
        ReferenceId = attrs.get('ReferenceId')
        if  not ReferenceId:
            raise serializers.ValidationError()
        return attrs

class SmileValidateEmailAddressSerializer(serializers.Serializer):
    """smart spPayments serializer."""
    EmailAddress = serializers.CharField()

    def validate(self, attrs):

        EmailAddress = attrs.get('EmailAddress')
        if not EmailAddress:
            raise serializers.ValidationError()
        return attrs



class SmileValidatePhoneSerializer(serializers.Serializer):
    
    PhoneNumber = serializers.CharField()

    def validate(self, attrs):

        PhoneNumber = attrs.get('PhoneNumber')
        if not PhoneNumber:
            raise serializers.ValidationError()
        return attrs



class ImpalRequestDemoSerializer(serializers.Serializer):
    """smart spPayments serializer."""
    api_username = serializers.CharField()
    api_password = serializers.CharField()

    def validate(self, attrs):
        api_username = attrs.get('api_username')
        api_password = attrs.get('api_password')
        if not api_username or not api_password:
            raise serializers.ValidationError()
        return attrs

class ImpalSendMoneySerializer(serializers.Serializer):
    """smart spPayments serializer."""
    session_id = serializers.CharField()
    source_country_code = serializers.CharField()
    sendername = serializers.CharField()
    recipient_mobile = serializers.CharField()
    amount = serializers.CharField()
    recipient_currency_code = serializers.CharField()
    recipient_country_code = serializers.CharField()
    reference_number = serializers.CharField()
    sendertoken = serializers.CharField()

    def validate(self, attrs):
        session_id = attrs.get('session_id')
        source_country_code = attrs.get('source_country_code')
        if not session_id or not source_country_code:
            raise serializers.ValidationError()
        return attrs



class ImpalBankTransferSerializer(serializers.Serializer):
    """smart spPayments serializer."""
    session_id = serializers.CharField()
    source_country_code = serializers.CharField()
    sendername = serializers.CharField()
    recipient_mobile = serializers.CharField()
    recipient_currency_code = serializers.CharField()
    recipient_country_code = serializers.CharField()
    reference_number = serializers.CharField()
    bank_code = serializers.CharField()
    amount = serializers.CharField()
    sender_address = serializers.CharField()
    sender_city = serializers.CharField()
    recipientname = serializers.CharField()
    accountnumber = serializers.CharField()



    def validate(self, attrs):
        session_id = attrs.get('session_id')
        source_country_code = attrs.get('source_country_code')
        if not session_id or not source_country_code:
            raise serializers.ValidationError()
        return attrs


class ImpalBalanceSerializer(serializers.Serializer):
    """smart spPayments serializer."""
    session_id = serializers.CharField()
    def validate(self, attrs):
        session_id = attrs.get('session_id')
        if not session_id:
            raise serializers.ValidationError()
        return attrs


class ImpalTranStausSerializer(serializers.Serializer):
    """smart spPayments serializer."""
    reference_number = serializers.CharField()
    def validate(self, attrs):
        reference_number  = attrs.get('reference_number')
        if not reference_number:
            raise serializers.ValidationError()
        return attrs



class ImpalXRateSerializer(serializers.Serializer):
    """smart spPayments serializer."""
    session_id = serializers.CharField()
    fromct = serializers.CharField()
    to = serializers.CharField()
    def validate(self, attrs):
        session_id = attrs.get('session_id')
        fromct = attrs.get('fromct')
        if not session_id or not fromct:
            raise serializers.ValidationError()
        return attrs


class ImpalVerifyBenSerializer(serializers.Serializer):
    """smart spPayments serializer."""
    session_id = serializers.CharField()
    first_name = serializers.CharField()
    second_name = serializers.CharField()
    last_name = serializers.CharField()
    mobile_number = serializers.CharField()
    country_code = serializers.CharField()
    def validate(self, attrs):
        session_id = attrs.get('session_id')
        first_name = attrs.get('fromct')
        if not session_id or not first_name:
            raise serializers.ValidationError()
        return attrs


class ImpalmsisdnBalSerializer(serializers.Serializer):
    """smart spPayments serializer."""
    session_id = serializers.CharField()
    country_code = serializers.CharField()
    def validate(self, attrs):
        session_id = attrs.get('session_id')
        country_code = attrs.get('country_code')
        if not session_id or not country_code:
            raise serializers.ValidationError()
        return attrs



class BeyonicPaymentsSerializer(serializers.Serializer):
    """smart spPayments serializer."""
    phonenumber = serializers.CharField()
    currency = serializers.CharField()
    sender = serializers.CharField()
    amount = serializers.CharField()
    description = serializers.CharField()
    payment_type = serializers.CharField()
    def validate(self, attrs):
        phonenumber = attrs.get('phonenumber')
        currency = attrs.get('currency')
        sender = attrs.get('sender')
        amount = attrs.get('amount')
        description = attrs.get('description')
        payment_type = attrs.get('payment_type')
        if not phonenumber or not currency or not sender or not amount or not description or not payment_type:
            raise serializers.ValidationError()
        return attrs


class BeyonicCollectionRequestsSerializer(serializers.Serializer):
    """smart spPayments serializer."""
    phonenumber = serializers.CharField()
    currency = serializers.CharField()
    amount = serializers.CharField()
    my_id = serializers.CharField()
    def validate(self, attrs):
        phonenumber = attrs.get('phonenumber')
        currency = attrs.get('currency')
        amount = attrs.get('amount')
        my_id = attrs.get('my_id')

        if not phonenumber or not currency  or not amount or not my_id:
            raise serializers.ValidationError()
        return attrs
