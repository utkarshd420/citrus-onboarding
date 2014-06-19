from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    application_status = models.CharField(max_length=2, choices=APPLICATION_STATUS_CHOICES, default=NEW, db_index=True)
    
    def __unicode__(self):
        return self.name


class CompanyCategory(models.Model):
    category = models.CharField(max_length = 300)
    def __unicode__(self):
        return self.category

class BusinessType(models.Model):
    type = models.CharField(max_length = 200)
    def __unicode__(self):
        return self.type


class Company(models.Model):
    name = models.CharField(max_length=100)
    merchant = models.ForeignKey(Merchant)
    company_category = models.ForeignKey(CompanyCategory)
    business_type = models.ForeignKey(BusinessType)
    def __unicode__(self):
        return "%s,%s,%s,%s" %(self.name,self.merchant,self.company_category,self.business_type)


class Bank(models.Model):
    bank = models.CharField(max_length = 200,unique=True)
    email = models.EmailField()
    def __unicode__(self):
        return self.bank


class MerchantBankApproval(models.Model):
    APPROVED = "A"
    PENDING = "P"
    INSUFFICIENT_DOCUMENTS = "ID"
    EMAIL_SENT = "ES"
    APPLICATION_STATUS_CHOICES = (
                                   (APPROVED, "Approved"),
                                   (PENDING, "Pending"),
                                   (INSUFFICIENT_DOCUMENTS, "Insufficient Documents"),
                                   (EMAIL_SENT,"Email Sent"),
                                   )
    merchant = models.ForeignKey(Merchant)
    bank = models.ForeignKey(Bank)
    status = models.CharField(max_length=2, choices=APPLICATION_STATUS_CHOICES, default=PENDING, db_index=True)
    remarks = models.CharField(max_length=320,blank=True) 
    date_mailed_on = models.DateTimeField(null=True, blank=True)
    date_received_status = models.DateTimeField(null=True, blank=True)
    employee_assigned_to = models.ForeignKey(User,blank=True,null=True,editable=False)


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

class bank_commercial(models.Model):
    bank = models.ForeignKey(Bank)
    company_category = models.ForeignKey(CompanyCategory)
    bank_commercial_value = models.CharField(max_length=15)
    #commercial =  models.ForeignKey ('commercial',blank=True,null=True)
    def __unicode__(self):
        return "%s,%s,%s" % (self.bank.bank,self.company_category.category,self.bank_commercial_value)

class commercial(models.Model):
    bank = models.ForeignKey(Bank)
    commercial_value = models.CharField(max_length=15,blank=True,null=True)
    merchant_commercial = models.ForeignKey('merchant_commercial')
    def __unicode__(self):
        return "%s,%s,%s" % (self.merchant_commercial,self.bank,self.commercial_value)

class merchant_commercial(models.Model):
    #merchant = models.ForeignKey(Merchant)
    company = models.ForeignKey(Company)
    def __unicode__(self):
        return "%s" % (self.company.name)
    def Merchant(self):
        return self.company.merchant
    def Company (self):
        return self.company.name
    def Company_category(self):
        return self.company.company_category

'''def __unicode__(self):
    return "%s\n%s" % (self.bank_commercial,self.merchant_commercial)'''

@receiver(post_save, sender=Company)
def create_commercial(sender,instance,created,**kwargs):
    if created:
        temp_merchant_commercial = merchant_commercial (company = instance)
        temp_merchant_commercial.save()
        all_banks = Bank.objects.all()
        for bank_obj in all_banks:
            temp_commercial = commercial(bank=bank_obj,commercial_value="1.2%",merchant_commercial=temp_merchant_commercial)
            temp_commercial.save()

@receiver(post_save, sender=Bank)
def create_bank_commercial(sender,instance,created,**kwargs):
    if created:
        for obj in CompanyCategory.objects.all():
            temp = bank_commercial(bank=instance,company_category=obj,bank_commercial_value="1.5%")
            temp.save()  
#def create_user_profile(sender, instance, created, **kwargs):  
#    if created:  
#        profile, created = Merchant.objects.get_or_create(user=instance)  
#
#post_save.connect(create_user_profile, sender=User)   
