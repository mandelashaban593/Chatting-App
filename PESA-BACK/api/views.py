'''default api view for remitapi'''
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from remitapi.authentication import ApiAuthentication
from django.conf import settings
from api.serializers import DepositMoneySerializer,TransactionStatusSerializer
from api.utils import ApiResponse, validate_number
from api.network_extensions import COUNTRY, NETWORK


class ApiView(APIView):
    """
    Default Api View Class
    """
    authentication_classes = (
        ApiAuthentication,
        )
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (JSONParser,)


class DepositMoneyRouter(ApiView):
	"""
	Route DepositMoney Calls
	"""
	serializer_class = DepositMoneySerializer


	def post(self, request):
		'''
		route query
		'''
		exception = None
		response = {}
		responsecode = 7
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			responsecode = 0
			msisdn = serializer.validated_data['phonenumber']
			amount = serializer.validated_data['amount']
			valid, responsecode, countrycode, networkcode = validate_number(msisdn)
			if not valid:
				if responsecode == 12:
					response['errors'] = {'The country code %s is not supported' % countrycode}
				elif responsecode == 13:
					response['errors'] = {'The network code %s is not supported for country code %s' % (
					networkcode,
					countrycode
					)}
			else:
				if countrycode == COUNTRY.UGANDA:
					'''dealing with uganda'''
					if networkcode in NETWORK.MTN_UGANDA:
						from mtn.views import MtnDepositMoney
						responsecode, response, exception = MtnDepositMoney(msisdn, amount, request.user)
				if countrycode == COUNTRY.KENYA:
					'''dealing with kenya'''
					from ipay.views import IpayDepositMoney
					responsecode, response, exception = IpayDepositMoney(msisdn, amount, request.user)
		else:
			response['errors'] = serializer.errors
		return ApiResponse(
		responsecode, response, exception
		)

class TransactionStatus(ApiView):
    """
    Route TransactionsStatus calls
    """
    print ':Transaction status view reached'
    serializer_class = TransactionStatusSerializer

    def post(self,request):
        """
        route query
        """
        print ':post data',str(request.data)
        print ':Transaction post reached'

        exception = None
        response = {}
        responsecode = 7
        serializer = self.serializer_class(data=request.data)
        utilitybill = None

        if serializer.is_valid():
            print ':Serializer valid'
            responsecode = 0
            transaction_id = serializer.validated_data['transaction_id']
            #transaction_type = serializer.validated_data['transaction_type']
            transid = int(transaction_id)
            for utility in UtilityTransaction.objects.all():
                if utility.app_ptr.transactionid == transid:
                    print ':Utility id found'
                    utilitybill = utility
                else:
                    print 'utility not found'

            if utilitybill is not None:
                response['utility_billtype'] = utiliybill.billtype

        else:
            print ':Serializer not valid'
            responsecode = 7
            response['errors'] = serializer.errors

        return ApiResponse(
            responsecode,response,exception
        )



        # else:
        #     response['errors'] = serializer.errors
        # return ApiResponse(
        # responsecode, response, exception
        # )
