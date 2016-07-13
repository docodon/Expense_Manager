from django.shortcuts import render
from mngr.models import Account_details,Transaction_details
from django.views.generic import View
from mngr.forms import UserForm,Account_form,Transaction_form,Login_form,Tag_form
from django.contrib.auth import authenticate, login , logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from copy import deepcopy
# Create your views here.


class register(View):
	def get(self,request):
		if request.user.is_authenticated():	
			return render_user_home(request,"User already logged in !")
		return render(request,"mngr/register.html",{'form':UserForm})
	
	def post(self,request):
		user_form = UserForm(data=request.POST)
		if user_form.is_valid() :
			user=user_form.save()
			user.set_password(user.password)
			user.save()
			return render(request,"mngr/index.html",{'form':Login_form,"message":'User added !'})
		else :
			return render(request,"mngr/register.html",{'form':Login_form,"message":'User added !'})

class Index(View):
	def get(self,request):
		if request.user.is_authenticated():	
			return render_user_home(request,"User already logged in !")
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
		return render_user_home(request,message=str(form.errors))	


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
			account2=Account_details.objects.get(account_num=instance.receiving_account)
			account2.balance-=instance.amount
		instance.delete()
		return render_user_home(request,message='Transaction removed')


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
def add_transaction(request):
	if request.method=='POST':
		form=Transaction_form(request,request.POST)
		if form.is_valid():
			typ_t=form.cleaned_data['type_trans']
			acc_details=form.cleaned_data['account_rel']
			amount=form.cleaned_data['amount']	
			if typ_t=='Credit':
				amount_credited(acc_details,form)
				return render_user_home(request,message='Amount credited !')
			else :
				if acc_details.balance<amount :
					return render_user_home(request,message='Insufficient funds !')
				if typ_t=='Debit':
					amount_debited(acc_details,form)
					return render_user_home(request,message='Amount debited !')
				if typ_t=='Transfer':
					val=amount_transfered(acc_details,form)
					if val==-1 :
						return render_user_home(message='Receiving account account is invalid !')
					return render_user_home(request,message='Fund transfered !')
		else :
			return render_user_home(request,message=form.errors)
	else :
		return redirect('/userhome/')


@login_required
def transaction_form(request):
	form = Transaction_form(request,request.POST)
	return render(request,"mngr/transaction_form.html",{'form':form})


@login_required
def account_form(request):
	return render(request,"mngr/account_form.html",{'form':Account_form})

@login_required
def search_tag(request):
	if request.method=='POST':
		form=Tag_form(request.POST)
		if form.is_valid():
			tag=form.cleaned_data['search_by_tag']
			trans_list=Transaction_details.objects.filter(account_rel__user=request.user,transaction_hashtags__icontains=tag)
			return render_user_home(request,list_trans=trans_list,tag=tag)
	return render_user_home(request)


def render_user_home(request,message=None,list_trans=None,tag=None):
	user_dict={}
	user_dict['acc_list']=Account_details.objects.filter(user=request.user)
	if list_trans==None:
		user_dict['trans_list']=Transaction_details.objects.filter(account_rel__user=request.user)
	else :
		user_dict['trans_list']=list_trans
		user_dict['tagged']=tag
		
	user_dict['Tag_form']=Tag_form
	if message is not None :
		user_dict['message']=message
	
	return render(request,'mngr/userhome.html',user_dict)	


def render_transaction_details(request,tran_obj,message=None):
	return render(request,"mngr/transaction_details.html",{'details':tran_obj})

		
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
	acc_num2=form.cleaned_data['receiving_account']
	
	try:
		acc_details2=Account_details.objects.get(account_num=acc_num2)
	except Account_details.DoesNotExist :
		acc_details2=None

	if acc_details2 is None :
		return -1

	amount_debited(acc_details,form)
	acc_details2.balance+=amount
	acc_details2.save()
	
	trans2=Transaction_details()
	trans2.account_rel=acc_details2
	trans2.type_trans='Transfer'
	trans2.receiving_account=acc_details.account_num
	trans2.transaction_hashtags=form.cleaned_data['transaction_hashtags']
	trans2.transaction_desc=form.cleaned_data['transaction_desc']
	trans2.amount=form.cleaned_data['amount']
	trans2.save()


