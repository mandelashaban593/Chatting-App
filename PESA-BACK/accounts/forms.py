'''form for adding user prfile'''
from django import forms
from registration.forms import RegistrationForm
from accounts.models import UserProfile,  UserActions, LoginInfo
from django.contrib.admin.models import LogEntry

'''
class TransactionForm(forms.ModelForm):
	"""
	Form for Adding an app
	"""
	class Meta:
		model = Transaction
		fields = '__all__'
		exclude = ('added', )
'''

class CustomRegistrationForm(RegistrationForm):
    '''custom registration form'''
    username = forms.CharField(widget=forms.HiddenInput(), required=False)


class LoginForm(forms.Form):
    '''custom registration form'''
    username = forms.CharField(label="Username",required=True,)
    password = forms.CharField(label="Password",required=True, widget=forms.PasswordInput())



class AdminLoginForm(forms.Form):
    '''custom registration form'''
    username = forms.CharField(label="Username",required=True,)
    password = forms.CharField(label="Password",required=True, widget=forms.PasswordInput())


class ChangeProfileForm(forms.ModelForm):
	"""
	Form for Adding an app
	"""
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)
	profile_pic = forms.ImageField(required=False)
	phonenumber = forms.RegexField(regex=r'^\+?1?\d{9,15}$', 
                                error_message = ("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))



	class Meta:
		model = UserProfile
		fields = '__all__'
		exclude = ('added', )


class ChangePasswordForm(forms.Form):
	"""
	Form for Adding an app
	"""
	current_password = forms.CharField(required=True)
	new_password = forms.CharField(required=True)
	confirm_new_password = forms.CharField(required=True)


	def __init__(self, user, data=None):
		self.user = user
		super(ChangePasswordForm, self).__init__(data=data)

	def clean(self):
		cleaned_data = super(ChangePasswordForm, self).clean()
		pass1 = cleaned_data['new_password']
		pass2 = cleaned_data['confirm_new_password']
		if not pass1 == pass2:
			raise forms.ValidationError("You passwords don't match ...")
		valid = self.user.check_password(self.cleaned_data['current_password'])
		if not valid:
			raise forms.ValidationError("Your Password is Incorrect...")
		return cleaned_data




class UserActionsForm(forms.ModelForm):

    """Form for saving user details on signup"""
    class Meta:
        model = UserActions
        fields = ['session', 'log_entry', 'user']


class LoginInfoForm(forms.ModelForm):

    """Form for saving user details on signup"""
    class Meta:
        model = LoginInfo
        fields = ['user_agent', 'remote_addr', 'user']



class LogEntryForm(forms.ModelForm):

    """Form for saving user details on signup"""
    class Meta:
        model = LogEntry
        fields = ['user', 'content_type', 'object_id',
         'object_repr', 'action_flag', 'change_message']