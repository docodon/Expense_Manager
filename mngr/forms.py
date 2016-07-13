from django import forms
from mngr.models import Transaction_details,Account_details
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from tagging.models import Tag

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta :
		model=User
		fields =['username', 'email', 'password']

class Account_form(forms.ModelForm):
	class Meta :
		model=Account_details
		exclude=['user','date_added']
		

class Transaction_form(forms.ModelForm):
	account_rel=forms.ModelChoiceField(queryset=Account_details.objects.none(),label='User account')
	
	class Meta :
		model=Transaction_details
		exclude=['transaction_date']
		fields=['account_rel','receiving_account','type_trans','amount','transaction_desc','transaction_hashtags']

	def __init__(self, request, *args, **kwargs):
		super(Transaction_form, self).__init__(*args, **kwargs)
		if request.user:
			queryset=Account_details.objects.filter(user=request.user)
		else:
			queryset = Searches.objects.all()
		self.fields['account_rel'].queryset = queryset



class Login_form(forms.Form):
	username=forms.CharField(max_length=100)
	password = forms.CharField(max_length=100,widget=forms.PasswordInput())

	
class Tag_form(forms.Form):
	search_by_tag= forms.ModelChoiceField(queryset=Tag.objects.all())
