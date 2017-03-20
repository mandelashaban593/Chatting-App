"""
remitapi URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings


urlpatterns = [
	url(r'^$', 'remitapi.views.landing_page', name='landing_page'),
	url(r'^wallet/', include('wallet.urls')),
	url(r'^tos$', 'remitapi.views.landing_page', name='tos'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('api.urls')),

    url(r'^api/v1/', include('api.v1.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^docs/', include('docs.urls')),
    url(r'^backend/', include('backend.urls')),



  url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
 {'document_root': settings.STATIC_ROOT,
 'show_indexes': False}
 ),
url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
 {'document_root': settings.MEDIA_ROOT,
 'show_indexes': False}
 ),
]
