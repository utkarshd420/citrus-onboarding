from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from signup.models import *

class serviceAdmin (admin.ModelAdmin):
	fields= ('name', 'charges', 'included_in_default')
	list_display = ('name', 'charges', 'included_in_default')

admin.site.register(Service,serviceAdmin)

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

class bankCommercialAdmin(admin.ModelAdmin):
	fields = (('bank','company_category'))
	list_display = ('bank','company_category')
	inlines = [bankCommercialInline]

admin.site.register(bank_commercial,bankCommercialAdmin)


class merchantAdmin(admin.ModelAdmin):
	fields = ('user','name','phone','url','application_status','step')
	list_display = ('user','name','phone','url','application_status','step')

class companyAdmin(admin.ModelAdmin):
	fields = ('name','merchant','company_category','business_type','friendly_name')
	list_display = ('name','friendly_name','get_merchant_name','get_merchant_phone','get_merchant_url','get_merchant_step','get_merchant_applicationStat','get_last_changed','company_category','business_type','get_file_list')

admin.site.register(Company,companyAdmin)

class companycategoryAdmin(admin.ModelAdmin):
	fields = ('category',('bank_commercial_citrus','mode_bank'),('merchant_commercial_citrus','mode_merchant'))
	list_display = ('category','merchant_rate','bank_rate')

admin.site.register(CompanyCategory,companycategoryAdmin)