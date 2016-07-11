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
)