from django.db import models
#from django.contrib.auth.models import User
from signup.models import Merchant, Company, MerchantBankApproval
import xlwt,datetime

class Bank_user_record (models.Model):
	bank = models.ForeignKey('Bank')
	bank_name = models.CharField(max_length=200)
	merchant = models.ForeignKey(Merchant)
	PENDING = "P"
	REJECTED = "R"
	APPLICATION_STATUS_CHOICES = ((PENDING, "Pending"),(REJECTED, "Rejected"))
	application_status = models.CharField(max_length=2, choices=APPLICATION_STATUS_CHOICES, default=PENDING, db_index=True)
	remarks = models.CharField(max_length=200)
	date_mailed_on = models.DateTimeField()
	date_received_status = models.DateTimeField(null=True, blank=True)
    

class Bank (models.Model):
	name = models.CharField(max_length = 200)
	email = models.EmailField()

	def unapproved_users(self,choiceList): ##creates the excel sheet
		unapp_user = Merchant.objects.filter(application_status = "N")
		workbook = xlwt.Workbook();
		worksheet = workbook.add_sheet(self.name)
		rowVal=0;colVal=0;
		worksheet.write(rowVal,colVal,"S.No.")
		colVal = colVal + 1

		####Header Region
		if (choiceList.merchant_name == True):
			worksheet.write(rowVal,colVal,"Merchant Name")
			colVal = colVal+1
		if (choiceList.merchant_friendly_name == True):
			worksheet.write(rowVal,colVal,"Merchant Friendly Name")
			colVal = colVal+1
		if (choiceList.merchant_url == True):
			worksheet.write(rowVal,colVal,"Merchant Website")
			colVal = colVal+1
		if (choiceList.merchant_region == True):
			worksheet.write(rowVal,colVal,"Merchant Region")
			colVal = colVal+1
		if (choiceList.merchant_category == True):
			worksheet.write(rowVal,colVal,"Merchant Category")
			colVal = colVal+1
		if (choiceList.merchant_commercial == True):
			worksheet.write(rowVal,colVal,"Merchant Commercials")
			colVal = colVal+1
		if (choiceList.merchant_type == True):
			worksheet.write(rowVal,colVal,"Merchant Type")
			colVal = colVal+1
		if (choiceList.merchant_address == True):
			worksheet.write(rowVal,colVal,"Merchant Address")
			colVal = colVal+1
		if (choiceList.bank_share == True):
			worksheet.write(rowVal,colVal,"Bank Share")
			colVal = colVal+1
		if (choiceList.bank_code == True):
			worksheet.write(rowVal,colVal,"Bank Code")
			colVal = colVal+1
		if (choiceList.expected_no_txn == True):
			worksheet.write(rowVal,colVal,"Expected no. of Txn")
			colVal = colVal+1
		if (choiceList.expected_no_vol == True):
			worksheet.write(rowVal,colVal,"Expected No. of Volume")
			colVal = colVal+1
		if (choiceList.requested_date == True):
			worksheet.write(rowVal,colVal,"Requested Date")
			colVal = colVal+1
		if (choiceList.status == True):
			worksheet.write(rowVal,colVal,"Status")
			colVal = colVal+1
		if (choiceList.confirmation == True):
			worksheet.write(rowVal,colVal,"Confirmation")
			colVal = colVal+1
		colVal=0
		rowVal= rowVal +1
		##header stops, body starts
		for obj in unapp_user:
			p= Bank_user_record(bank= self,bank_name= self.name,merchant= obj,date_mailed_on=datetime.datetime.now())
			p.save()
			worksheet.write(rowVal,colVal,rowVal)
			colVal= colVal+1
			worksheet.write(rowVal,colVal,obj.name)
			colVal= colVal+1
			worksheet.write(rowVal,colVal,obj.user.email)
			colVal= colVal+1
			worksheet.write(rowVal,colVal,obj.phone)
			colVal= colVal+1
			rowVal= rowVal+1
			colVal=0
		workbook.save("Files/"+self.name+".xlsx")
		return unapp_user

class BankChoice (models.Model):
	##Fields that are supoosed to be included in the bank approval sheet
	bank = models.ForeignKey(Bank)
	merchant_name = models.BooleanField(default=True)
	merchant_friendly_name = models.BooleanField(default=True)
	merchant_url = models.BooleanField(default=True)
	merchant_region = models.BooleanField(default=True)
	merchant_category = models.BooleanField(default=True)
	merchant_commercial = models.BooleanField(default=True)
	merchant_type = models.BooleanField(default=True)
	bank_share = models.BooleanField(default=True)
	expected_no_txn = models.BooleanField(default=True)
	expected_no_vol = models.BooleanField(default=True)
	requested_date = models.BooleanField(default=True)
	status = models.BooleanField(default=True)
	confirmation = models.BooleanField(default=True)
	bank_code = models.BooleanField(default=True)
	merchant_address = models.BooleanField(default=True)


