'''url api views'''
import mtn.views as views
from django.conf.urls import patterns, url
from rest_framework import routers
router = routers.DefaultRouter()


urlpatterns = patterns('',
   
    url(r'^checknumber/(?P<msisdn>[0-9\w]+)', views.CheckNumber.as_view()),
    url(r'^depositmoney/$', views.DepositMoney.as_view()),
    url(r'^withdrawmoney/$', views.WithdrawMoney.as_view()),
    url(r'^transactionstatus/$', views.TransactionStatus.as_view()),
    url(r'^transaction/(?P<transactionid>[0-9\w]+)',
    	views.Transaction.as_view()
    ),
    url(r'^transactions/', views.Transaction.as_view()),
)
