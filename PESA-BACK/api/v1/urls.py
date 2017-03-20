from django.conf.urls import patterns, include, url
import api.v1.views as views


urlpatterns = patterns('',


	url(r'^momo/depositmoney/$', views.DepositMoneyRouter.as_view()),
	url(r'^paybill/queryaccount/$', views.PaybillQueryAccountRouter.as_view()),
	url(r'^paybill/querypaytv/$', views.PaybillQueryTvBouquet.as_view()),
	url(r'^paybill/$', views.PaybillRouter.as_view()),
	url(r'^paybill/transactionstatus/$', views.PaybillGetTransactionRouter.as_view()),
    url(r'^transactionstatus/$',views.TransactionStatus.as_view()),
	url(r'^tlance/deposit/$',views.TradelanceDeposit.as_view()),
	url(r'^tlance/requestpayment/$',views.TradelanceRequestPayment.as_view()),
	url(r'^tlance/transactionstatus/$',views.TradelanceTransactionStatus.as_view()),
	url(r'^tlance/balancecheck/$',views.Tradelancebalancecheck.as_view()),
	url(r'^tlance/accountstatement/$',views.TradelanceAccountStatement.as_view()),
	url(r'^tlance/fundstransfer/$',views.TradelanceFundsTransfer.as_view()),
	url(r'^smart/payments/$',views.SmartPayments.as_view()),
	url(r'^smart/status/$',views.SmartTransStatus.as_view()),
	url(r'^smart/withdrawdeposit/$',views.SmartWithdrawDeposit.as_view()),
	url(r'^smart/sendreceive/$',views.SmartSendReceiveMoney.as_view()),
	url(r'^smart/airtimetopup/$',views.SmartAirtimeTopup.as_view()),
	url(r'^sendsms/residentclient/$',views.ResidentClientSmsRouter.as_view()),
	url(r'^sendsms/client/$',views.ClientSmsRouter.as_view()),

	url(r'^notifs/register/$',views.RegisterNotifClientRouter.as_view()),
	url(r'^notifs/mobile/send/$',views.SendMobileNotifRouter.as_view()),
	url(r'^rwanda/queryaccount/$',views.RwandaQueryAccount.as_view()),
	url(r'^rwanda/paybill/$',views.RwandaEnquirePayment.as_view()),
	url(r'^rwanda/confirmpay/$',views.RwandaConfirmPayment.as_view()),
	url(r'^rwanda/retrypaybill/$',views.RwandaRetryPayment.as_view()),
	url(r'^rwanda/reissuepayment/$',views.RwandaReissuePayment.as_view()),
	url(r'^rwanda/paymentminihistoryperproduct/$',views.RwandaPaymentMiniHistoryPerProduct.as_view()),
	url(r'^rwanda/getTodayMinireport/$',views.RwandaGetTodayMiniReport.as_view()),
	url(r'^rwanda/getdailyMinireport/$',views.RwandaGetDailyMiniReport.as_view()),
	url(r'^rwanda/getthismonthminireport/$',views.RwandaGetThisMonthMiniReport.as_view()),
	url(r'^beyonic/collectionrequests/$',views.BeyonicCollectionRequests.as_view()),
	url(r'^beyonic/payments/$',views.BeyonicPayments.as_view()),

	url(r'^smile/authenticate/$',views.SmileAuthenticate.as_view()),
	url(r'^smile/balancequery/$',views.SmileBalanceQuery.as_view()),
	url(r'^smile/balancetransfer/$',views.SmileBalanceTransfer.as_view()),
	url(r'^smile/validateaccountquery/$',views.SmileValidateAccountQuery.as_view()),
	url(r'^smile/bundlecataloguequery/$',views.SmileBundleCatalogueQuery.as_view()),
	url(r'^smile/buybundle/$',views.SmileBuyBundle.as_view()),
	url(r'^smile/transactionstatusquery/$',views.SmileTransactionStatusQuery.as_view()),
	url(r'^smile/newcustomer/$',views.SmileNewCustomer.as_view()),
	url(r'^smile/validatereferenceid/$',views.SmileValidateReferenceId.as_view()),
	url(r'^smile/validateemailaddress/$',views.SmileValidateEmailAddress.as_view()),
	url(r'^smile/validatephone/$',views.SmileValidatePhone.as_view()),
	url(r'^impala/requestdemo/$',views.ImpalRequestDemo.as_view()),
	url(r'^impala/requestsessionid/$',views.ImpalReqSesid.as_view()),
	url(r'^impala/sendmoney/$',views.ImpalSendMoney.as_view()),
	url(r'^impala/banktransfer/$',views.ImpalBankTransfer.as_view()),
	url(r'^impala/balance/$',views.ImpalBalance.as_view()),
	url(r'^impala/transtaus/$',views.ImpalTranStaus.as_view()),
	url(r'^impala/xchangerate/$',views.ImpalXRate.as_view()),
	url(r'^impala/verifybeneficiary/$',views.ImpalVerifyBen.as_view()),
	url(r'^impala/msisdnbalance/$',views.ImpalmsisdnBal.as_view()),











	#url(r'^smart/guardian/$',views.SmartGuardian.as_view()),

#PaybillGetTransactionRouter

)
