from django.db import models
#from django.contrib.auth.models import User
from signup.models import Merchant, Company, MerchantBankApproval, Bank
import xlwt,datetime

class BankChoice (models.Model):
	##Fields that are supoosed to be included in the bank approval sheet
	bank = models.ForeignKey(Bank)
	merchant_name = models.BooleanField(default=True)
	merchant_friendly_name = models.BooleanField(default=True)
	merchant_url = models.BooleanField(default=True)
	merchant_region = models.BooleanField(default=True)
	merchant_category = models.BooleanField(default=True)
	merchant_commercial = models.BooleanField(default=True)
	merchant_type = models.BooleanField(default=True)
	bank_share = models.BooleanField(default=True)
	expected_no_txn = models.BooleanField(default=True)
	expected_no_vol = models.BooleanField(default=True)
	requested_date = models.BooleanField(default=True)
	status = models.BooleanField(default=True)
	confirmation = models.BooleanField(default=True)
	bank_code = models.BooleanField(default=True)
	merchant_address = models.BooleanField(default=True)


