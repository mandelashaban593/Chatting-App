'''
accounts urls
'''
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'wallet.views.landing_page', name='wallet'),
    url(r'^signup/$', 'accounts.views.signup', name='registration_register'),
    url(r'^login/$', 'accounts.views.user_login',name='login'),
    url(r'^logout/$', 'accounts.views.signout',name='logout'),
    url(r'^api_keys/$', 'dashboard.views.api_keys',name='api_keys'),
)
