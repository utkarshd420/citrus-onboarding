from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
class Merchant(models.Model):
  user = models.OneToOneField(User)
  name = models.CharField(max_length=100)
  phone = models.CharField(max_length=15)
  step = models.IntegerField(default=1)
  def __unicode__(self):
    return self.company_name
class MerchantCompany(models.Model):
  merchant = models.ForeignKey(Merchant)
  company_name = models.CharField(max_length=100)
  company_category = models.CharField(max_length=100)
  business_type = models.CharField(max_length=100)
class ApprovedBank(models.Model):
  merchant = models.ForeignKey(Merchant)
  bank_name = models.CharField(max_length=100) 
class CompanyCategory(models.Model):
  categorylist = models.CharField(max_length = 300)
class BusinessType(models.Model):
  typelist = models.CharField(max_length = 200)
class Services(models.Model):
  servicename = models.CharField(max_length = 200)
  servicecost = models.IntegerField(default = 0)
class Bank(models.Model):
  banklist = models.CharField(max_length = 200)
def create_user_profile(sender, ins:tance, created, **kwargs):  
  if created:  
    profile, created = new.objects.get_or_create(user=instance)  
post_save.connect(create_user_profile, sender=User)   
