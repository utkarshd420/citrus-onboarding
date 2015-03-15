from django.db import models
from signup.models import Merchant, CompanyCategory, BusinessType, Company


class pg_Bank(models.Model):
    bank = models.CharField(max_length = 200,unique=True)
    email = models.EmailField()
    def __unicode__(self):
        return self.bank

class pg_Choice(models.Model):
	pg_Choice = models.CharField(max_length = 200)
	def __unicode__(self):
		return self.pg_Choice	


class pg_BankChoice (models.Model):
	##Fields that are supoosed to be included in the bank approval sheet
	bank = models.ForeignKey(pg_Bank)
	choice = models.ForeignKey(pg_Choice)
	include = models.BooleanField(default=False)
	def __unicode__(self):
		return str(self.choice)



class PaymentMode(models.Model):
	mode = models.CharField(max_length=200)
	#bank = models.ForeignKey(pg_Bank)
	def __unicode__(self):
		return self.mode

class CardScheme(models.Model):
	scheme = models.CharField(max_length=200)
	def __unicode__(self):
		return self.scheme


































