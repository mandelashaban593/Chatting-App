'''admin configurations'''
from django.contrib import admin
from mtn.models import MtnTransaction 
from registration.models import RegistrationProfile
from registration.admin import RegistrationAdmin


#remove registration
try:
	admin.site.unregister(RegistrationProfile)
	admin.site.unregister(RegistrationAdmin)
except Exception:
	pass

admin.site.register(MtnTransaction)
