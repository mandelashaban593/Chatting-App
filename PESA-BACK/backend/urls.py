"""
remitapi URL Configuration
"""
from django.conf.urls import patterns, include, url
import backend.views as backend
import remitapi.settings as settings

urlpatterns = patterns('',
                          url(r'^$', 'backend.views.home', name="backend"),

                            
                          
                          url(r'^login/$', backend.admin_login, name="backend_login"),

                          url(r'^audits/$', backend.audits_trails,name="audits_trails"),

                           url(r'^export_data/$', backend.export_data,name="export_data"),
                           url(r'^users/admin/add/$', 
                               backend.create_stuff_user,name="create_admin_user"),

                           url(r'^users/admin/add/cc/$', 
                               backend.create_customer_care_user,name="create_customer_care_user"),

                           url(r'^users/admin/$', 
                               backend.stuff_users,name="view_admin_user"),


                           url(r'^customer_care/transactions/search/$', 
                               backend.phonenumber_transaction_search,name="cc_transaction_search"),
                           

                           url(r'^users/admin/edit/(\w+)/$', 
                               backend.edit_stuff_user,name="edit_admin_user"),

                           url(r'^reports/$', 
                               backend.reports,name="admin_reports"),
                           url(r'^users/blockuser/$', 
                               backend.block_user,name="admin_block_user"),
                           url(r'^users/unblockuser/$', 
                               backend.unblock_user,name="admin_unblock_user"),
                           url(r'^users/verifyuser/$', 
                               backend.verify_user,name="admin_verify_user"),
                           url(r'^users/unverifyuser/$', 
                               backend.unverify_user,name="admin_unverify_user"),
                           url(r'^users/(\w+)/$', 
                               backend.users,name="admin_users"),
                           url(r'^user/(\w+)/contact/$', 
                               backend.contact_user,name="contact_user"),
                           url(r'^transactions/resend/$', 
                               backend.resend_transaction,name="admin_resend_transaction"),
                           url(r'^transactions/process/$', 
                               backend.process_transaction,name="admin_process_transaction"),
                           url(r'^transactions/(\w+)/$', 
                               backend.transactions,name="admin_transactions"),
                            url(r'^transactions/(\w+)/(\w+)/$', 
                               backend.transactions,name="admin_user_transactions"),

                            url(r'^transaction/(\w+)/receipt/$', 
                               backend.transaction_receipt,name="transaction_receipt"),

                           url(r'^transaction/(\w+)/edit/$', 
                               backend.edit_transaction,name="edit_transaction"),
                           url(r'^transaction/(\w+)/$', 
                               backend.view_transaction,name="admin_transaction"),
                           url(r'^user/(\w+)/$', 
                               backend.user,name="admin_user"),
                           url(r'^rates/(?P<code>.+)/$', 
                               backend.rates,name="admin_rates"),
                           url(r'^charges_limits/(?P<code>.+)/$', 
                               backend.charges_limits,name="admin_charges_limits"),
                           url(r'^logs/$', 
                               backend.logs,name="admin_logs"),
                           
                           #url(r'^seo/$','seo.views.seo', name="admin_seo"),

                           url(r'^logout/$', 'django.contrib.auth.views.logout',
                            {'next_page': settings.BASE_URL } , name="admin_logout"),

                           
                           # url(r'^users/$', backend.users),name="admin_verified_users"),

)
