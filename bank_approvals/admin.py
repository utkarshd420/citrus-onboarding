from django.contrib import admin
from django.contrib import messages
from bank_approvals.models import BankChoice , receive_mail_banks
import os,xlrd
from signup.models import Company, MerchantBankApproval, Bank
from e import *
from create_email import *
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver

def unapproved_users(modeladmin,request,bank_obj,choiceList): 
	unapp_user = MerchantBankApproval.objects.filter(status = "P", bank=bank_obj)
	body_mail = '''Dear Sir/Ma'am,

Please find attached the  new merchant addition list on Citrus - %s Net Banking payment platform.  
Request your approval for the same.

_______________________________________________

Thanks and Regards,
Citrus Payment Solutions Pvt. Ltd.
					''' %(bank_obj.bank)
					
	subject_mail= ''' %s - Citrus_Merchant addition_ %s'''%(bank_obj.bank,str(datetime.now().strftime('%d.%m.%Y')))

	if(len(unapp_user)==0):
		message="No user with pending status"
		modeladmin.message_user (request,message)
	else:
		dirname = create_workbook(bank_obj,choiceList,unapp_user)
		try:
			emailtemp=bank_obj.email
			email = EmailMessage(subject_mail, body_mail, 'vasughatole@gmail.com', [''+emailtemp])
			email.attach_file(dirname+"/"+bank_obj.bank+".xls")
			email.send()
			message = "Email sent to "+bank_obj.bank
			modeladmin.message_user(request,message)
			for obj in unapp_user:
				obj.status= "ES"
				obj.date_mailed_on=datetime.now()
				obj.employee_assigned_to = request.user
				obj.save()
		except Exception, e:
			message="Email not sent to bank "+bank_obj.bank+ " Error raised: "+str(e)
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
			print (row[merchantCol])
			bank_approval_temp = MerchantBankApproval.objects.get(bank=bank,company__name = unicode(row[merchantCol]))
			company_temp = Company.objects.get(company__name= bank_approval_temp.company)
			if (row[statusCol].lower() == "approved"):
				bank_approval_temp.status = "A"
				company_temp.merchant.application_status = "IP"
			elif (row[statusCol].lower() == "insufficient documents"):
				bank_approval_temp.status = "ID"
				company_temp.merchant.application_status = "R"
			else:
				bank_approval_temp.status = "P"
				company_temp.merchant.application_status = "R"
			bank_approval_temp.remarks = row[remarkCol]
			company_temp.save()
			bank_approval_temp.save()
def email_banks(modeladmin, request, queryset): 
	for obj in queryset: 
		choiceList = BankChoice.objects.filter(bank=obj)[0]
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
	list_display = ('bank','company','status','remarks','employee_assigned_to','date_mailed_on','date_received_status')

class ReceiveEmail (admin.ModelAdmin):
	list_display = ('bank','status','file_name','date_changed_on')
	actions = [receive_email,reset_status]


@receiver(post_save, sender=Bank)
def create_bank_commercial(sender,instance,created,**kwargs):
    if created:
        temp = receive_mail_banks(bank=instance,status="NR") 
        temp.save()


admin.site.register(Bank,BankAdmin)
admin.site.register(MerchantBankApproval,RecordAdmin)
admin.site.register(receive_mail_banks,ReceiveEmail)
