from django.contrib import admin
from .models import Account_details,Transaction_details

# Register your models here.

admin.site.register(Account_details)
admin.site.register(Transaction_details)