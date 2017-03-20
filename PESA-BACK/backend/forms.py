'''ModelForms for Admin'''
from django import forms
from remitapi.models import ApiTransaction, Charge
from accounts.models import UserProfile
from backend.models import EmailSupport
from django.contrib.auth.models import User


class TransactionUpdateForm(forms.ModelForm):

    """
    Form for updating transactions
    """
    class Meta:
        model = ApiTransaction
        fields = ['app', ]


class ProfileUpdateForm(forms.ModelForm):

    """
    Form for updating user profile
    """
    class Meta:
        model = UserProfile
        fields = ['firstname', 'lastname', ]


class ProfileAddForm(forms.ModelForm):

    """
    Form for migrating user profile
    """
    class Meta:
        model = UserProfile
        fields = ['user', ]


class TransactionAddForm(forms.ModelForm):

    """
    Form for migrating user phonebook
    """
    class Meta:
        model = ApiTransaction
        fields = ['app',
                  ]


class CreateAdminUserForm(forms.ModelForm):

    """
    Form for migrating user phonebook
    """

    password2 = forms.CharField(required=True, max_length=255)
    rates = forms.CharField(required=True, max_length=1)
    transactions = forms.CharField(required=True, max_length=1)
    users = forms.CharField(required=True, max_length=1)
    reports = forms.CharField(required=True, max_length=200)
    email = forms.EmailField(required=True, max_length=255)
    network = forms.CharField(required=True, max_length=20)
    country = forms.CharField(required=True, max_length=20)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean(self):

        # check passwords
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError('Username already taken.')
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email is already taken.')
        return data



class EditAdminUserForm(forms.ModelForm):

    """
    Form for migrating user phonebook
    """

    password2 = forms.CharField(required=False, max_length=255)
    password = forms.CharField(required=False, max_length=255)
    rates = forms.CharField(required=True, max_length=1)
    transactions = forms.CharField(required=True, max_length=1)
    users = forms.CharField(required=True, max_length=1)
    reports = forms.CharField(required=True, max_length=200)
    email = forms.EmailField(required=True, max_length=255)
    network = forms.CharField(required=True, max_length=20)
    country = forms.CharField(required=True, max_length=20)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean(self):

        # check passwords
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data

    def clean_username(self):
        data = self.cleaned_data['username']
        if not data == self.instance.username:
            raise forms.ValidationError('Invalid Stuff Username, Dont Change these Values')
        return data


    def clean_email(self):
        data = self.cleaned_data['email']
        if not data == self.instance.email:
            raise forms.ValidationError('Invalid Stuff Email, Dont Change these Values')
        return data



class ContactUserForm(forms.ModelForm):

    """
    Form for migrating user phonebook
    """
    class Meta:
        model = EmailSupport
        fields = ['user',
                  'msg',
                  'subject',
                  'support_staff',
                   ]


class transactionPhonenumberSearchForm(forms.Form):
    phonenumber = forms.CharField(required = True, label = "Phonenumber to search",
        max_length = 60)


class ChargesLimitsForm(forms.ModelForm):
    '''charges limits form'''
    class Meta(object):
        """docstring for Meta"""
        model=Charge
        #fields = '__all__'
        fields = ['forex_percentage', 'transfer_fee_percentage', 'transfer_maximum_usd',
        'transfer_minimum_usd','general_network_charge','mtn_charge','airtel_charge','safaricom_charge']
            
        

class RateUpdateForm(forms.ModelForm):

    """
    Form for updating rates
    """
    class Meta:
        model = Charge
        fields = ['to_usd', 'to_gbp', 'to_eur']

