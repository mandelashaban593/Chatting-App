from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    url(r'^$', 'dashboard.views.home', name='home'),
    url(r'^mobilemoney$', 'dashboard.views.mobilemoney', name='momo'),
    url(r'^billpayments/reports/$', 'dashboard.views.billreports', name='billreports'),
    #url(r'^creditcard$', 'dashboard.views.creditcard', name='cc'),
    #url(r'^billpayments$', 'dashboard.views.billpayments', name='billpayments'),


)
