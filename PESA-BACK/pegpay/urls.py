
from django.conf.urls import patterns, url, include
from rest_framework import routers, serializers
#from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
router = routers.DefaultRouter()
import pegpay.views as views

urlpatterns = patterns('',

    #query user
    url(r'^query_account/$',views.QueryAccount.as_view()),


    #utility urls
    url(r'^utilities/water/$',views.WaterTransaction.as_view()),


    url(r'^utilities/electricity/$',views.ElectricityTransaction.as_view()),


)
