from django import forms
from mngr.models import Transaction_details,Account_details
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta :
		model=User
		fields =['username', 'email', 'password']

class Account_form(forms.ModelForm):
	class Meta :
		model=Account_details
		exclude=['user']

class Transaction_form(forms.ModelForm):
	account_num=forms.IntegerField()
	class Meta :
		model=Transaction_details
		exclude=['account_rel']

class Login_form(forms.Form):
	username=forms.CharField(max_length=100)
	password = forms.CharField(max_length=100,widget=forms.PasswordInput())


