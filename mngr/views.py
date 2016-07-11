from django.shortcuts import render
from mngr.models import Account_details,Transaction_details
from django.views.generic import View
from mngr.forms import UserForm,Account_form,Transaction_form,Login_form
from django.contrib.auth import authenticate, login , logout

# Create your views here.

class Index(View):
	def get(self,request):
			return render(request,"mngr/index.html",{'form':Login_form})
	
	def post(self):
		form=Login_form(request.POST)
		if form.is_valid():
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None and user.is_active() :
				login(request,user)
         		return userhome(request)
         	else:
				return render( request , "mngr/index.html" , {'form':Login_form,'message':'Username not in our database !' } )
		return render(request,"mngr/index.html",{'form':Login_form,'message':form.errors}) 

def amount_credited(acc_details,form):
	amount=form.cleaned_data['amount']
	acc_details.balance+=amount
	acc_details.save()
	new_trans=form.save(commit=False)
	new_trans.account_rel=acc_details
	new_trans.save()
	
def amount_debited(acc_details,form):
	amount=form.cleaned_data['amount']
	acc_details.balance-=amount
	acc_details.save()
	new_trans=form.save(commit=False)
	new_trans.account_rel=acc_details
	new_trans.amount=-amount
	new_trans.save()
					
def amount_transfered(acc_details,form):
	amount=form.cleaned_data['amount']
	acc_num2=form.cleaned_data['second_account']
	acc_details2=Account_details.get(account_num=acc_num2)
	
	if acc_details2 is none :
		return render_user_home('Second account is invalid !')
				
	amount_debited(acc_details,form)

	acc_details2.balance+=amount
	acc_details2.save()
	new_trans2=form.save(commit=False)
	new_trans2.account_rel=acc_details2
	new_trans2.second_account=acc_num
	new_trans2.save()				


def render_user_home(request,message=None):
	user_dict={}
	user_dict['form1']=Account_form
	user_dict['form2']=Transaction_form
	acc_list=Account_details.objects.filter(user=request.user)
	
	trans_list=Transaction_details.objects.filter(account_rel=request.user)
	
	if message is not None :
		user_dict['message']=message
	return render(request,'mngr/userhome.html',user_dict)	


class userhome(View):
	def get(self,request):
		return render_user_home(request)

	def post(self,request):
		form=Account_form(request.POST)
		if form.is_valid():
			new_account=form.save(commit=False)
			new_account.user=request.user
			new_account.save()
			return render_user_home('Account added !')	
		else :
			form=Transaction_form(request.POST)
			
			if form.is_valid():
				acc_num=form.cleaned_data['account_num']
				typ_t=form.cleaned_data['type_trans']
				acc_details=Account_details.get(account_num=acc_num)
				
				if acc_details is none  or acc_details.user != request.user:
					return render_user_home(request,'Invalid account !')
				
				if typ_t=='Credit':
					amount_credited(acc_details,form)
					return render_user_home(request,'Amount credited !')
				else :
					if account_details.balance<amount :
						return render_user_home(request,'Insufficient funds !')
					if typ_t=='Debit':
						amount_debited(acc_details,form)
						return render_user_home(request,'Amount debited !')
					if typ_t=='Transfer':
						amount_transfered(acc_details,form)
						return render_user_home(request,'Fund transfered !')
			





