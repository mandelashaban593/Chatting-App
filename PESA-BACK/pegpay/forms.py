from django import forms
from django.forms import ModelForm
from models import WaterTransaction,ElectricityTransaction




class WaterTransactionForm(ModelForm):
    '''water transaction form'''
    class Meta:
        model = WaterTransaction
        fields = ['customer_ref','customer_name','customer_phone','paid_by','amount','sender_message','company_code','area']


class ElectricityTransactionForm(ModelForm):
    '''electricity transaction form'''
    class Meta:
        model = ElectricityTransaction
        fields = ['customer_type','payment_type','sender_message','customer_ref','customer_name','customer_phone','paid_by','amount','customer_email','company_code']
