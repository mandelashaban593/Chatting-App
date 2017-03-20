from django.conf.urls import patterns, include, url
import api.views as views


urlpatterns = patterns('',


	#url(r'^DepositMoney/$','api.views.DepositMoneyRouter'),
	url(r'^momo/depositmoney/$', views.DepositMoneyRouter.as_view()),
	#url(r'^WithdrawMoney/$','api.views.WithdrawMoneyRouter'),
	#url(r'^AccountDetails/$','api.views.WithdrawMoneyRouter'),
    #url(r'^transactionstatus/$',views.TransactionStatus.as_view()),

    url(r'^momo/mtn/', include('mtn.urls')),
    url(r'^momo/', include('ipay.urls')),
    url(r'^paybill/', include('pegpay.urls')),

)
