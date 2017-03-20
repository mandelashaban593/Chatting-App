'''forms for the remitapi api'''
from django import forms


class WithdrawMoneyForm(forms.Form):
	phonenumber = forms.CharField(required=True, max_length=20)
	amount = forms.CharField(required=True, max_length=20)