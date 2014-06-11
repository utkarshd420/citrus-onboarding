from django.contrib import admin
from django.contrib import messages
from bank_approvals.models import BankChoice
import os
from datetime import datetime
import xlwt
from signup.models import Company, MerchantBankApproval, Bank
from django.core.mail import send_mail
#from django.core.management.base import NoArgsCommand
from django.core.mail.message import EmailMessage

def unapproved_users(modeladmin,request,bank_obj,choiceList): 
		unapp_user = MerchantBankApproval.objects.filter(status = "P")
		if(len(unapp_user)==0):
			message="No user with pending status"
			modeladmin.message_user (request,message)
		else:
			workbook = xlwt.Workbook();
			worksheet = workbook.add_sheet(bank_obj.bank)
			rowVal=0;colVal=0;
			style_string = """font:bold on;
							  border:left thick,top thick,bottom thick,right thick;
							  alignment:horizontal center,vertical center;
							  pattern:pattern solid,fore_color gray25"""
			header_style = xlwt.easyxf(style_string)

			worksheet.write(rowVal,colVal,"S.No.",style=header_style)
			colVal = colVal + 1
			##############Header Region############################
			if (choiceList.merchant_name == True):
				worksheet.write(rowVal,colVal,"Merchant Name",style=header_style)
				colVal = colVal+1
			if (choiceList.merchant_friendly_name == True):
				worksheet.write(rowVal,colVal,"Merchant Friendly Name",style=header_style)
				colVal = colVal+1
			if (choiceList.merchant_url == True):
				worksheet.write(rowVal,colVal,"Merchant Website",style=header_style)
				colVal = colVal+1
			if (choiceList.merchant_region == True):
				worksheet.write(rowVal,colVal,"Merchant Region",style=header_style)
				colVal = colVal+1
			if (choiceList.merchant_category == True):
				worksheet.write(rowVal,colVal,"Merchant Category",style=header_style)
				colVal = colVal+1
			if (choiceList.merchant_commercial == True):
				worksheet.write(rowVal,colVal,"Merchant Commercials",style=header_style)
				colVal = colVal+1
			if (choiceList.merchant_type == True):
				worksheet.write(rowVal,colVal,"Merchant Type",style=header_style)
				colVal = colVal+1
			if (choiceList.merchant_address == True):
				worksheet.write(rowVal,colVal,"Merchant Address",style=header_style)
				colVal = colVal+1
			if (choiceList.bank_share == True):
				worksheet.write(rowVal,colVal,"Bank Share",style=header_style)
				colVal = colVal+1
			if (choiceList.bank_code == True):
				worksheet.write(rowVal,colVal,"Bank Code",style=header_style)
				colVal = colVal+1
			if (choiceList.expected_no_txn == True):
				worksheet.write(rowVal,colVal,"Expected no. of Txn",style=header_style)
				colVal = colVal+1
			if (choiceList.expected_no_vol == True):
				worksheet.write(rowVal,colVal,"Expected No. of Volume",style=header_style)
				colVal = colVal+1
			if (choiceList.requested_date == True):
				worksheet.write(rowVal,colVal,"Requested Date",style=header_style)
				colVal = colVal+1
			if (choiceList.status == True):
				worksheet.write(rowVal,colVal,"Status",style=header_style)
				colVal = colVal+1
			if (choiceList.confirmation == True):
				worksheet.write(rowVal,colVal,"Confirmation",style=header_style)
				colVal = colVal+1
			colVal=0
			rowVal= rowVal +1
			####################header stops, body starts#####################3
			dirname=str(datetime.now().strftime('%Y.%m.%d'))
			#d = os.path.dirname(dirname)
			if not os.path.exists('./'+dirname+'/'):
				os.makedirs("%s"%dirname)

			workbook.save(dirname+"/"+bank_obj.bank+".xlsx")
			try:
				emailtemp=bank_obj.email
				email = EmailMessage('subject of the mail ', 'body of the mail', 'vasughatole@gmail.com', [''+emailtemp])
				email.attach_file(dirname+"/"+bank_obj.bank+".xlsx")
				email.send()
				for obj in unapp_user:
					obj.status= "ES"
					obj.date_mailed_on=datetime.now()
					obj.save()
			except Exception, e:
				message="Email not sent to bank "+bank_obj.bank
				modeladmin.message_user (request,message,"error")
			
			
			return unapp_user
#################################################


def email_banks(modeladmin, request, queryset): 
	for obj in queryset: 
		choiceList = BankChoice.objects.get(bank=obj)
		unapproved_users(modeladmin,request,obj,choiceList)

email_banks.short_description = "Email the selected banks all Pending users"
class BankChoiceInline(admin.StackedInline):
	model = BankChoice
	extra = 0;

class BankAdmin (admin.ModelAdmin):
	fieldsets = [
        ('Bank Info', {'fields': ['bank','email']}),
       
    ]
	inlines = [BankChoiceInline]
	list_display = ('bank','email')
	actions = [email_banks]

class RecordAdmin (admin.ModelAdmin):
	list_display = ('bank','merchant','status','remarks','date_mailed_on','date_received_status')

admin.site.register(Bank,BankAdmin)
admin.site.register(MerchantBankApproval,RecordAdmin)
	
