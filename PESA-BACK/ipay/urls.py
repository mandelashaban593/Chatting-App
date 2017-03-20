'''url api views'''
import ipay.views as views
from django.conf.urls import patterns, url
from rest_framework import routers
router = routers.DefaultRouter()


urlpatterns = patterns('',

    url(r'^mpesa/depositmoney/$', views.DepositMoney.as_view(network='mpesa')),
    url(r'^airtel/depositmoney/$', views.DepositMoney.as_view(network='airtel')),

)
