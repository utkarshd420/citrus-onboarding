from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
import datetime, random
class Merchant(models.Model):
    NEW = "N"
    REJECTED = "R"
    IN_PROGRESS = "IP"
    ONBOARDING_COMPLETED = "OC"
    DROPPED = "DP"
    APPLICATION_STATUS_CHOICES = (
                                   (NEW, "New"),
                                   (REJECTED, "Rejected"),
                                   (IN_PROGRESS, "In Progress"),
                                   (ONBOARDING_COMPLETED, "Completed"),
                                   (DROPPED,"Dropped"),
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
    last_changed_on = models.DateTimeField(default=datetime.datetime.now())
    verified_account = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name


class CompanyCategory(models.Model):
    category = models.CharField(max_length = 300)
    bank_commercial_citrus = models.DecimalField(max_digits=10,decimal_places=2)
    PERCENTAGE = "PERC"
    RUPEES = "INR"
    mode_choices = (
                    (PERCENTAGE,"%"),
                    (RUPEES,"INR")
                    )
    mode_bank = models.CharField(max_length=4, choices=mode_choices, default=PERCENTAGE, db_index=True)
    merchant_commercial_citrus = models.DecimalField(max_digits=10,decimal_places=2)
    mode_merchant = models.CharField(max_length=4, choices=mode_choices, default=PERCENTAGE, db_index=True)
    def __unicode__(self):
        return self.category
    def merchant_rate(self):
        if (self.mode_merchant == "PERC"):
            return str(self.merchant_commercial_citrus) + " % " 
        else:
            return str(self.merchant_commercial_citrus) + " Rs. "
    def bank_rate(self):
        if (self.mode_bank == "PERC"):
            return str(self.bank_commercial_citrus) + " % " 
        else:
            return str(self.bank_commercial_citrus) + " Rs. "

class BusinessType(models.Model):
    type = models.CharField(max_length = 200)
    def __unicode__(self):
        return self.type


class Company(models.Model):
    name = models.CharField(max_length=100)
    merchant = models.ForeignKey(Merchant)
    company_category = models.ForeignKey(CompanyCategory)
    business_type = models.ForeignKey(BusinessType)
    friendly_name = models.CharField(max_length=200,blank=True,null=True)
    def __unicode__(self):
        return "%s,%s,%s,%s" %(self.name,self.merchant,self.company_category,self.business_type)
    def get_merchant_name(self):
        return self.merchant.name
    get_merchant_name.short_description = 'Merchant Name'
    def get_merchant_user(self):
        return self.merchant.user
    get_merchant_user.short_description = 'Merchant User'
    def get_merchant_phone(self):
        return self.merchant.phone
    get_merchant_phone.short_description = 'Merchant Phone Number'
    def get_merchant_url(self):
        return self.merchant.url
    get_merchant_url.short_description = 'Merchant URL'
    def get_merchant_applicationStat(self):
        if(self.merchant.application_status == 'N'):
            return "New"
        if(self.merchant.application_status == 'R'):
            return "Rejected"
        if(self.merchant.application_status == 'IP'):
            return "In Progress"
        if(self.merchant.application_status == 'OC'):
            return "Onboarding Completed"
    get_merchant_applicationStat.short_description = 'Merchant Application Status'
    def get_merchant_step(self):
        return self.merchant.step
    get_merchant_step.short_description = "Merchant Step"
    def get_file_list(self):
        curr_file_dir = os.getcwd()+"/files/"+self.merchant.user.email
        try:
            output = ""
            dir_list =  os.listdir(curr_file_dir)
            
            for dirs in dir_list:
                curr_file_temp_dir = curr_file_dir + "/"+dirs+"/"
                output+= "-------"+dirs+"------<br>"
                file_list = os.listdir(curr_file_temp_dir)
                for files in file_list:
                    output+= "<a href='%s'>%s</a><br>" %("/files/"+self.merchant.user.email+"/"+dirs+"/"+files,files)
            return output
        except Exception, e:
            return 
    get_file_list.allow_tags =True
    get_file_list.short_description = "Files Uploaded"
    def get_last_changed(self):
        return self.merchant.last_changed_on
    get_last_changed.short_description = "Last Changed"

    
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
    company = models.ForeignKey(Company)
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
    def __unicode__(self):
        return self.name


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
    verification_amount = models.DecimalField(decimal_places=2,max_digits=5,default= random.random()*10)
    verification_amount_sent_date = models.DateTimeField(blank=True,null=True)

class bank_commercial_value(models.Model):
    PERCENTAGE = "PERC"
    RUPEES = "INR"
    mode_choices = (
                    (PERCENTAGE,"%"),
                    (RUPEES,"INR"),
                    )
    value = models.DecimalField(max_digits=10,decimal_places=2)
    mode = models.CharField(max_length=4, choices=mode_choices, default=PERCENTAGE, db_index=True)
    from_merchant = models.BooleanField(default= False)
    bank_commercial = models.ForeignKey('bank_commercial')
    def __unicode__(self): 
        return str(self.value)+" "+str(self.mode)

class bank_commercial(models.Model):
    bank = models.ForeignKey(Bank)
    company_category = models.ForeignKey(CompanyCategory,blank=True,null=True)
    def __unicode__(self):
        return "%s,%s" % (self.bank.bank,self.company_category.category)

class commercial(models.Model):
    bank = models.ForeignKey(Bank)
    commercial_value = models.DecimalField(max_digits=10,decimal_places=2)
    PERCENTAGE = "PERC"
    RUPEES = "INR"
    mode_choices = (
                    (PERCENTAGE,"%"),
                    (RUPEES,"INR")
                    )
    mode = models.CharField(max_length=4, choices=mode_choices, default=PERCENTAGE, db_index=True)
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




class document(models.Model):
	header = models.CharField(max_length=200)
	doc_list = models.CharField(max_length=200)
	businessType = models.ForeignKey(BusinessType)
### Additional Merchant Details ###

class action_mail(models.Model):
	head=models.CharField(max_length=100)
	limit=models.IntegerField()
	age=models.IntegerField()

class document_user_status(models.Model):
		merchant=models.ForeignKey(Merchant)
		type=models.CharField(max_length=200)
		verified=models.BooleanField(default=False)
		uploaded=models.BooleanField(default=False)
		join_date=models.DateTimeField(default=datetime.datetime.now())
		last_reminder=models.DateTimeField(default=datetime.datetime.now())

class merchant_address(models.Model):
	flat_no = models.CharField(max_length=20,null=True,blank=True)
	building_name = models.CharField(max_length=150,null=True,blank=True)
	street_name = models.CharField(max_length=150,null=True,blank=True)
	road_name = models.CharField(max_length=150,null=True,blank=True)
	area_name = models.CharField(max_length=150,null=True,blank=True)
	city = models.CharField(max_length=150,null=True,blank=True)
	state = models.CharField(max_length=150,null=True,blank=True) 

class merchant_website_details(models.Model):
	#merchant = models.ForeignKey(Merchant)
	about_us_url = models.URLField(null=True,blank=True)
	contact_us_url = models.URLField(null=True,blank=True)
	terms_conditions_url = models.URLField(null=True,blank=True)
	prduct_description_url = models.URLField(null=True,blank=True)
	returns_refund_url = models.URLField(null=True,blank=True)
	privacy_policy_url = models.URLField(null=True,blank=True)
	shipping_delivery_url = models.URLField(null=True,blank=True)
	disclaimer_url = models.URLField(null=True,blank=True)


class additional_company_details(models.Model):
	merchant = models.ForeignKey(Merchant)
	address = models.ForeignKey(merchant_address)
	website_details = models.ForeignKey(merchant_website_details)
	date_of_establishment = models.DateTimeField()
	min_ticket_size = models.CharField(max_length=15)
	max_ticket_size = models.CharField(max_length=15)
	avg_monthly_volume = models.CharField(max_length=15)
	company_turnover = models.CharField(max_length=15)
	business_line = models.CharField(max_length=50)
	current_pg_service = models.CharField(max_length=200,blank=True,null=True)
	international_card_required = models.CharField(max_length=10)

        

class merchant_contact(models.Model):
	name = models.CharField(max_length=300)
	email = models.EmailField()
	contact_number = models.IntegerField(max_length=12)

class merchant_contact_details(models.Model):
	merchant = models.ForeignKey(Merchant)
<<<<<<< HEAD
	#merchant_business_contact = models.ForeignKey(merchant_contact,related_name="merchant_business_contact+")
	#merchant_operation_contact = models.ForeignKey(merchant_contact,related_name="merchant_operation_contact+")
	#merchant_customer_service = models.ForeignKey(merchant_contact,related_name="merchant_customer_service+")

=======
	merchant_business_contact = models.ForeignKey(merchant_contact,related_name="merchant_business_contact+",blank=True,null=True)
	merchant_operation_contact = models.ForeignKey(merchant_contact,related_name="merchant_operation_contact+",blank=True,null=True)
	merchant_customer_service = models.ForeignKey(merchant_contact,related_name="merchant_customer_contact+",blank=True,null=True)

class merchant_website_details(models.Model):
	#merchant = models.ForeignKey(Merchant)
	about_us_url = models.URLField()
	contact_us_url = models.URLField()
	terms_conditions_url = models.URLField()
	product_description_url = models.URLField()
	returns_refund_url = models.URLField()
	privacy_policy_url = models.URLField()
	shipping_delivery_url = models.URLField()
	disclaimer_url = models.URLField()
	website_status = models.CharField(max_length=10)
>>>>>>> 7d53252b58c779fae01bf7c8dba6ae3a3e2a2b03

class merchant_bank_details(models.Model):
	merchant = models.ForeignKey(Merchant)
	bank_name = models.CharField(max_length=200)
	branch_name = models.CharField(max_length=300)
	ifsc_code = models.CharField(max_length=20)
	account_number = models.CharField(max_length=30)
####################
class emailNEFT(models.Model):
	email  = models.EmailField()
	name = models.CharField(max_length=200,blank=True,null=True)


@receiver(post_save, sender=Company)
def create_commercial(sender,instance,created,**kwargs):
    if created:
        temp_merchant_commercial = merchant_commercial (company = instance)
        temp_merchant_commercial.save()
        all_banks = Bank.objects.all()
        for bank_obj in all_banks:
            temp_commercial = commercial(bank = bank_obj,commercial_value = (instance.company_category.merchant_commercial_citrus),mode=instance.company_category.mode_merchant,merchant_commercial=temp_merchant_commercial)
            temp_commercial.save()

@receiver(post_save, sender=Bank)
def create_bank_commercial(sender,instance,created,**kwargs):
    if created:
        for obj in CompanyCategory.objects.all():
            temp = bank_commercial(bank=instance,company_category=obj)
            temp.save()
            temp_bank_commercial = bank_commercial_value(value= obj.bank_commercial_citrus,mode = obj.mode_bank,bank_commercial= temp)
            temp_bank_commercial.save()

'''@receiver(post_save,sender=Merchant)
def update_last_changed(sender,instance,**kwargs):
	instance.last_changed_on = datetime.datetime.now()
	instance.save()'''

#def create_user_profile(sender, instance, created, **kwargs):  
#    if created:  
#        profile, created = Merchant.objects.get_or_create(user=instance)  
#
#post_save.connect(create_user_profile, sender=User)   
