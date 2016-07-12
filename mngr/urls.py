from django.conf.urls import patterns, url
from mngr import views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView


urlpatterns=patterns('',
	url(r'^index/$',views.Index.as_view(),name='Index'),
	url(r'^userhome/$',views.userhome.as_view(),name='userhome'),
	url(r'^register/$',views.register.as_view(),name='register'),
	url(r'^add_transaction/$',views.add_transaction,name='add_transaction'),
	url(r'^transaction_details/(?P<tran_id>[0-9]+)/$',views.transaction_details.as_view(),name='transaction_detail'),
	url(r'^acc_details/(?P<acc_id>[0-9]+)/$',views.acc_details,name='acc_details'),
	url(r'^logout/$','django.contrib.auth.views.logout',{'next_page':'/index/'}),
	url(r'^transaction_form/$',views.transaction_form,name='transaction_form'),
	url(r'^account_form/$',views.account_form,name='account_form'),
)