from django.shortcuts import render
from mngr.models import Account_details,Transaction_details
from django.views.generic import View
from mngr.forms import UserForm,Account_form,Transaction_form,Login_form
from django.contrib.auth import authenticate, login , logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

class Index(View):
	def get(self,request):
			return render(request,"mngr/index.html",{'form':Login_form})
	
	def post(self,request):
		form=Login_form(request.POST)
		if form.is_valid():
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('/userhome/')
		return render( request , "mngr/index.html" , {'form':Login_form,'message':'User not authorized !' } )
		
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
	try:
		acc_details2=Account_details.get(account_num=acc_num2)
	except Account_details.DoesNotExist :
		acc_details2=None

	if acc_details2 is None :
		return -1
				
	amount_debited(acc_details,form)

	acc_details2.balance+=amount
	acc_details2.save()
	new_trans2=form.save(commit=False)
	new_trans2.account_rel=acc_details2
	new_trans2.second_account=acc_num
	new_trans2.save()				

def render_user_home(request,message=None):
	user_dict={}
	user_dict['acc_list']=Account_details.objects.filter(user=request.user)
	user_dict['trans_list']=Transaction_details.objects.filter(account_rel__user=request.user)
	if message is not None :
		user_dict['message']=message
	return render(request,'mngr/userhome.html',user_dict)	


class userhome(View):
	@method_decorator(login_required)
	def get(self,request):
		return render_user_home(request)

	@method_decorator(login_required)
	def post(self,request):	
		form=Account_form(request.POST)
		if form.is_valid():
			new_account=form.save(commit=False)
			new_account.user=request.user
			new_account.save()
			return render_user_home(request,'Account added !')	
		return render_user_home(request,str(form.errors))	

@method_decorator(login_required)
def add_transaction(request):
	if request.method=='POST':
		form=Transaction_form(request.POST)
		if form.is_valid():
			acc_num=form.cleaned_data['account_num']
			typ_t=form.cleaned_data['type_trans']
				
			try:
   				acc_details=Account_details.objects.get(account_num=acc_num)
			except Account_details.DoesNotExist:
				acc_details = None

			if acc_details is None  or acc_details.user != request.user:
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
					val=amount_transfered(acc_details,form)
					if val==-1 :
						return render_user_home('Second account is invalid !')
					return render_user_home(request,'Fund transfered !')
		else :
			return render_user_home(request,form.errors)
	else :
		return redirect('/userhome/')

class register(View):
	@method_decorator(login_required)
	def get(self,request):
		return render(request,"mngr/register.html",{'form':UserForm})
	
	@method_decorator(login_required)
	def post(self,request):
		user_form = UserForm(data=request.POST)
		if user_form.is_valid() :
			user=user_form.save()
			user.set_password(user.password)
			user.save()
			return render(request,"mngr/index.html",{'form':Login_form,"message":'User added !'})
		else :
			return render(request,"mngr/register.html",{'form':Login_form,"message":'User added !'})

def render_transaction_details(request,tran_obj,message=None):
	return render(request,"mngr/transaction_details.html",{'details':tran_obj})

class transaction_details(View):
	@method_decorator(login_required)
	def get(self,request,tran_id):
		try:
			tran_obj=Transaction_details.objects.get(id=tran_id)
		except Transaction_details.DoesNotExist :
			return render_transaction_details(request,tran_obj,'Transaction does not exist !')
		if tran_obj.account_rel.user != request.user :
			return render_transaction_details(request,tran_obj,'Invalid Transaction !')
		return render_transaction_details(request,tran_obj)

	@method_decorator(login_required)
	def post(self,request,tran_id):
		instance = Transaction_details.objects.get(id=tran_id)
		if instance.type_trans=='Credit' or instance.type_trans=='Debit':
			instance.account_rel.balance-=instance.amount
		else :
			instance.account_rel.balance-=instance.amount
			account2=Account_details.objects.get(account_num=instance.second_account)
			account2.balance-=instance.amount
		instance.delete()
		return render_user_home(request,'Transaction removed')

@login_required
def acc_details(request,acc_id):
	try :
		acc_obj=Account_details.objects.get(id=acc_id)
		tran_set=Transaction_details.objects.filter(account_rel=acc_obj)
		if acc_obj.user != request.user :
			return render(request,"mngr/account_details.html",{'message':"Invalid account"})
		else :
			return render(request,"mngr/account_details.html",{'details':acc_obj,'tran_list':tran_set})
	except Account_details.DoesNotExist:
		return render(request,"mngr/account_details.html",{'message':'No such account !'})

@login_required
def transaction_form(request):
	return render(request,"mngr/transaction_form.html",{'form':Transaction_form})

@login_required
def account_form(request):
	return render(request,"mngr/account_form.html",{'form':Account_form})