from django.contrib import admin
from payment_gateway.models import pg_Bank, pg_Choice, pg_BankChoice, PaymentMode , CardScheme


class pg_BankChoiceInline(admin.TabularInline):
	model = pg_BankChoice
	fields = [('choice', 'include')]
	extra = 0;

class pg_BankAdmin(admin.ModelAdmin):
	fieldsets = [('PG Banks', {'fields': ['bank','email']})]
	list_display = ('bank','email')
	inlines = [pg_BankChoiceInline]
	#inlines = [pg_BankChoice]

#class PaymentModeAdmin(admin.ModelAdmin):


admin.site.register(PaymentMode)
admin.site.register(CardScheme)
admin.site.register(pg_Choice)
admin.site.register(pg_Bank, pg_BankAdmin)






















