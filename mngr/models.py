from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Account_details(models.Model):
	user=models.ForeignKey(User)
	account_num=models.IntegerField(unique=True)
	account_detail=models.CharField(max_length=100)
	balance=models.IntegerField()

TCHOICES=(('Credit','Credit'),('Debit','Debit'),('Transfer','Transfer'))


class Transaction_details(models.Model):
	account_rel=models.ForeignKey(Account_details)
	type_trans=models.CharField(max_length=100,choices=TCHOICES)
	second_account=models.IntegerField(blank=True)
	transaction_hashtag=models.CharField(max_length=100)
	transaction_desc=models.CharField(max_length=100)
	amount=models.IntegerField(max_length=100)
