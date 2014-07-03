from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from signup.models import *
from django.core.mail import send_mass_mail
import datetime


def send_alert(modeladmin,request,queryset):
	try:
		for obj in queryset:
			if(obj.head=='document upload reminder'):
				limit=obj.limit
				age=obj.age
				message=[]
				heading = 'Reminder '
				sender ='bank-relations@citruspay.com'
				msg = ''' This is a reminder from citruspay . Please upload the following documents from verification - 
	 				''' 
	 			drop_msg= ''' Your citrus account is dropped. Please contact citruspay for furthur assitance . '''
	 			compose=[heading,msg,sender,[]]
	 			merchants = Merchant.objects.all()
	 			for merchant in merchants:
					x=[]
					flag=0
					p=document_user_status.objects.filter(merchant=merchant)
					for obj in p:
						print obj.type
						if obj.uploaded==True:
							continue
						print int((datetime.datetime.now() - obj.last_reminder.replace(tzinfo=None)).days),limit
						if int((datetime.datetime.now()-obj.join_date.replace(tzinfo=None)).days) >= age:
							compose[1]=drop_msg
							compose[3]=[]
							compose[3].append(merchant.user.email)
							message.append(compose)
							merchant.application_status='DP'
							flag=1
							merchant.save()
							break
						if int((datetime.datetime.now() - obj.last_reminder.replace(tzinfo=None)).days) >= limit:
							x.append(obj.type)
							obj.last_reminder = datetime.datetime.now()
							obj.save()	
					print flag,len(x)
					if flag ==0 and len(x)!=0 :
						msg= msg + ' , '.join(x)
						compose[1]=msg
						compose[3]=[]
						compose[3].append(merchant.user.email)
						message.append(compose)
						print compose		   
			
			send_mass_mail(message,fail_silently=False)
			print message
			message = "Sent the alert to the selected entities"
			modeladmin.message_user (request,message)
				
	except Exception, e:
		message="Alert not sent Error raised: "+str(e)
		modeladmin.message_user (request,message,"error")
send_alert.short_description = "Alert all the entities for the selected email"
class alertsAdmin(admin.ModelAdmin):
	list_display = ('head','limit','age')
	fields = ('head','limit','age')
	actions = [send_alert]

admin.site.register(action_mail,alertsAdmin)

class serviceAdmin (admin.ModelAdmin):
	fields= ('name', 'charges', 'included_in_default')
	list_display = ('name', 'charges', 'included_in_default')

admin.site.register(Service,serviceAdmin)
class docAdmin(admin.ModelAdmin):
	list_display = ('merchant','type','verified','uploaded','join_date','last_reminder')
admin.site.register(document_user_status,docAdmin)

class commercialInline(admin.StackedInline):
	model = commercial
	extra = 0

'''class bankcommercialInline(admin.StackedInline):
	model = bank_commercial
	extra = 0 '''

class merchantCommercialAdmin(admin.ModelAdmin):
	#fields = ('merchant')
	list_display = ('Merchant','Company','Company_category')
	inlines = [commercialInline]

admin.site.register(merchant_commercial,merchantCommercialAdmin)

class bankCommercialInline(admin.StackedInline):
	model = bank_commercial_value
	extra = 0

class documentInline(admin.StackedInline):
	model = document
	extra = 0 

class bankCommercialAdmin(admin.ModelAdmin):
	fields = (('bank','company_category'))
	list_display = ('bank','company_category')
	inlines = [bankCommercialInline]

admin.site.register(bank_commercial,bankCommercialAdmin)


class merchantAdmin(admin.ModelAdmin):
	fields = ('user','name','phone','url','application_status','step','verified_account')
	list_display = ('user','name','phone','url','application_status','step','verified_account')
admin.site.register(Merchant,merchantAdmin)

class companyAdmin(admin.ModelAdmin):
	fields = ('name','merchant','company_category','business_type','friendly_name')
	list_display = ('name','friendly_name','get_merchant_name','get_merchant_phone','get_merchant_url','get_merchant_step','get_merchant_applicationStat','get_last_changed','company_category','business_type','get_file_list')

admin.site.register(Company,companyAdmin)

class companycategoryAdmin(admin.ModelAdmin):
	fields = ('category',('bank_commercial_citrus','mode_bank'),('merchant_commercial_citrus','mode_merchant'))
	list_display = ('category','merchant_rate','bank_rate')

admin.site.register(CompanyCategory,companycategoryAdmin)

class businessAdmin(admin.ModelAdmin):
	inlines = [documentInline]
admin.site.register(BusinessType,businessAdmin)