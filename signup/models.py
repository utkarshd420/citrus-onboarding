from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class Merchant(models.Model):
    NEW = "N"
    REJECTED = "R"
    IN_PROGRESS = "IP"
    ONBOARDING_COMPLETED = "OC"
    APPLICATION_STATUS_CHOICES = (
                                   (NEW, "New"),
                                   (REJECTED, "Rejected"),
                                   (IN_PROGRESS, "In Progress"),
                                   (ONBOARDING_COMPLETED, "Completed"),
                                   ) 
    
    STEP_SIGNUP = 1
    STEP_PAYMENT = 2
    STEP_IMPLEMENTATION = 3
    STEP_UPLOAD_DOCS = 4
    STEP_CHOICES = (
                    (STEP_SIGNUP,"Signup"),
                    (STEP_PAYMENT,"Payment"),
                    (STEP_IMPLEMENTATION,"Implementation"),
                    (STEP_UPLOAD_DOCS,"Upload Docs"),
                    )
    
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=15)
    url = models.URLField(max_length=200, unique=True)
    step = models.IntegerField(choices=STEP_CHOICES, default=STEP_SIGNUP)
    applicaton_status = models.CharField(max_length=2, choices=APPLICATION_STATUS_CHOICES, default=NEW, db_index=True)
    
    def __unicode__(self):
        return self.name


class CompanyCategory(models.Model):
    category = models.CharField(max_length = 300)


class BusinessType(models.Model):
    type = models.CharField(max_length = 200)


class Company(models.Model):
    name = models.CharField(max_length=100)
    merchant = models.ForeignKey(Merchant)
    company_category = models.ForeignKey(CompanyCategory)
    business_type = models.ForeignKey(BusinessType)


class Bank(models.Model):
    bank = models.CharField(max_length = 200)


class MerchantBankApproval(models.Model):
    APPROVED = "A"
    PENDING = "P"
    INSUFFICIENT_DOCUMENTS = "ID"
    APPLICATION_STATUS_CHOICES = (
                                   (APPROVED, "Approved"),
                                   (PENDING, "Pending"),
                                   (INSUFFICIENT_DOCUMENTS, "Insufficient Documents"),
                                   )
    merchant = models.ForeignKey(Merchant)
    bank = models.ForeignKey(Bank)
    status = models.CharField(max_length=2, choices=APPLICATION_STATUS_CHOICES, default=PENDING, db_index=True)
    remarks = models.CharField(max_length=320) 


class Service(models.Model):
    name = models.CharField(max_length=200)
    charges = models.IntegerField(default=0)
    included_in_default = models.BooleanField(default=False)


class MerchantService(models.Model):
    merchant = models.ForeignKey(Merchant)
    service = models.ForeignKey(Service)


class Txn(models.Model):
    SUCCESSFUL = "S"
    PENDING = "P"
    FAILED = "F"
    TRANSACTION_STATUS_CHOICES = (
                                   (SUCCESSFUL, "Successful"),
                                   (PENDING, "Pending"),
                                   (FAILED, "Failed"),
                                   )
    merchant_tx_id = models.CharField(max_length=64, db_index=True)
    merchant = models.ForeignKey(Merchant)
    status = models.CharField(max_length=2, choices=TRANSACTION_STATUS_CHOICES, default=PENDING, db_index=True)
    citrus_tx_id = models.CharField(max_length=64, null=True, db_index=True, blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    date_time = models.DateTimeField(null=True, db_index=True, blank=True)

def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
        profile, created = new.objects.get_or_create(user=instance)  

post_save.connect(create_user_profile, sender=User)   
