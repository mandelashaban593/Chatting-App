from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    
    url(r'^$', 'docs.views.home', name='docs_home'),
    url(r'^api$', 'docs.views.apidocs', name='apidocs'),


)
