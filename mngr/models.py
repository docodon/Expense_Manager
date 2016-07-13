from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from tagging.fields import TagField

# Create your models here.
class Account_details(models.Model):
	user=models.ForeignKey(User)
	account_num=models.IntegerField(unique=True)
	account_detail=models.CharField(max_length=100)
	balance=models.IntegerField()
	date_added= models.DateTimeField(default=timezone.now)

	def __unicode__(self):
		return str(self.account_num)

TCHOICES=(('Credit','Credit'),('Debit','Debit'),('Transfer','Transfer'))
		
class Transaction_details(models.Model):
	account_rel=models.ForeignKey(Account_details)
	type_trans=models.CharField(max_length=100,choices=TCHOICES)
	receiving_account=models.IntegerField(blank=True,null=True)
	transaction_hashtags= TagField(null=True,blank=True)
	transaction_desc=models.CharField(max_length=100)
	amount=models.IntegerField(max_length=100)
	transaction_date=models.DateTimeField(default=timezone.now)

	def __unicode__(self):
		return self.transaction_desc