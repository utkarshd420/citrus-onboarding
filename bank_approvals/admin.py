from django.contrib import admin
from django.contrib import messages
from bank_approvals.models import BankChoice , receive_mail_banks
import os,xlrd
from signup.models import Company, MerchantBankApproval, Bank
from e import *
from create_email import *
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage

def unapproved_users(modeladmin,request,bank_obj,choiceList): 
	unapp_user = MerchantBankApproval.objects.filter(status = "P", bank=bank_obj)
	if(len(unapp_user)==0):
		message="No user with pending status"
		modeladmin.message_user (request,message)
	else:
		dirname = create_workbook(bank_obj,choiceList)
		try:
			emailtemp=bank_obj.email
			email = EmailMessage('subject of the mail ', 'body of the mail', 'vasughatole@gmail.com', [''+emailtemp])
			email.attach_file(dirname+"/"+bank_obj.bank+".xlsx")
			email.send()
			for obj in unapp_user:
				obj.status= "ES"
				obj.bank_objdate_mailed_on=datetime.now()
				obj.employee_assigned_to = request.user
				obj.save()
		except Exception, e:
			message="Email not sent to bank "+bank_obj.bank+ "Error raised: "+str(e)
			modeladmin.message_user (request,message,"error")
		return unapp_user

def read_update(filePath,bank):
	workbook = xlrd.open_workbook(filePath)
	worksheets = workbook.sheet_names()
	for worksheet_name in worksheets:
		worksheet = workbook.sheet_by_name(worksheet_name)
		currRow = 0;merchantCol = 0; statusCol = 0; remarkCol = 0;
		num_rows = worksheet.nrows - 1
		row_obj = worksheet.row(currRow)
		row=[]
		for cell in row_obj:
				row.append(cell.value)
		print(row)
		merchantCol = row.index("Merchant Name")
		statusCol = row.index("Status")
		remarkCol = row.index("Remarks")
		while (currRow < num_rows):
			currRow +=1
			row_obj = worksheet.row(currRow)
			row=[]
			for cell in row_obj:
				row.append(cell.value)
			bank_approval_temp = MerchantBankApproval.objects.get(bank=bank,merchant__name = row[merchantCol])
			if (row[statusCol].lower() == "approved"):
				bank_approval_temp.status = "A"
			elif (row[statusCol].lower() == "insufficient documents"):
				bank_approval_temp.status = "ID"
			else:
				bank_approval_temp.status = "P"
			bank_approval_temp.remarks = row[remarkCol]
			bank_approval_temp.save()
def email_banks(modeladmin, request, queryset): 
	for obj in queryset: 
		choiceList = BankChoice.objects.get(bank=obj)
		unapproved_users(modeladmin,request,obj,choiceList)

email_banks.short_description = "Email the selected banks all Pending users"

def receive_email(modeladmin, request, queryset):
	for bank_obj in queryset:
		try:
			fileName = email_rec(bank_obj)
			filePath = 'received file/'+fileName
			read_update(filePath,bank_obj.bank)
			bank_obj.status = "ER"
			bank_obj.file_name = fileName
			bank_obj.date_changed_on = datetime.now()
			bank_obj.save()

		except Exception, e :
				message="Email not received or net error Exception raised:  "+ str(e)
				modeladmin.message_user (request,message,"error")

receive_email.short_description = "Catch the response files from the banks"

def reset_status(modeladmin, request, queryset):
	for obj in queryset:
		obj.status = "NR"
		obj.file_name = ""
		obj.date_changed_on = datetime.now()
		obj.save()		
reset_status.short_description = "Reset status of selected banks"
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
	list_display = ('bank','merchant','status','remarks','employee_assigned_to','date_mailed_on','date_received_status')

class ReceiveEmail (admin.ModelAdmin):
	list_display = ('bank','status','file_name','date_changed_on')
	actions = [receive_email,reset_status]

admin.site.register(Bank,BankAdmin)
admin.site.register(MerchantBankApproval,RecordAdmin)
admin.site.register(receive_mail_banks,ReceiveEmail)
