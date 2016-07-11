from django.conf.urls import patterns, url
from mngr import views

urlpatterns=patterns('',
	url(r'^index/$',views.Index.as_view(),name='Index'),
	url(r'^userhome/$',views.userhome.as_view(),name='userhome'),
	)