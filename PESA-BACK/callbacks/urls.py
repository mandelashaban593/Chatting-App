from django.conf.urls import patterns, url, include
from . import views
import callbacks.views as views

urlpatterns = [
   
    url(r'^africas/$', views.process_africas, name='process_africas'),
     url(r'^beyonic/collections/$', views.process_beyonic, name='process_beyonic'),
    url(r'^beyonic/payment$', views.process_payment2, name='process_beyonic'),
]



