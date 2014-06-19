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


class bankCommercialAdmin(admin.ModelAdmin):
	fields = (('bank','company_category'),'bank_commercial_value')
	list_display = ('bank','company_category','bank_commercial_value')

admin.site.register(bank_commercial,bankCommercialAdmin)


