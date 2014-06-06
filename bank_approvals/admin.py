from django.contrib import admin
from bank_approvals.models import Bank,BankChoice,Bank_user_record

def email_banks(modeladmin, request, queryset): 
	for obj in queryset: 
		choiceList = BankChoice.objects.get(bank=obj)
		obj.unapproved_users(choiceList)

email_banks.short_description = "Email the selected banks all Pending users"
class BankChoiceInline(admin.StackedInline):
	model = BankChoice
	extra = 0;

class BankAdmin (admin.ModelAdmin):
	fieldsets = [
        ('Bank Info',               {'fields': ['name','email']}),
       
    ]
	inlines = [BankChoiceInline]
	list_display = ('name','email')
	actions = [email_banks]

class RecordAdmin (admin.ModelAdmin):
	list_display = ('bank_name','merchant','application_status','remarks','date_mailed_on','date_received_status')

admin.site.register(Bank,BankAdmin)
admin.site.register(Bank_user_record,RecordAdmin)
	
