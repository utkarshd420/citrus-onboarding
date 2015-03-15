import xlwt, datetime

#######Creates excel sheet#######################
def unapproved_users(modeladmin,request,bank_obj,choiceList): 
		unapp_user = MerchantBankApproval.objects.filter(status = "P")
		if(len(unapp_user)==0):
			message="No user with pending status"
			modeladmin.message_user (request,message)
		else:
			workbook = xlwt.Workbook();
			worksheet = workbook.add_sheet(bank_obj.bank)
			rowVal=0;colVal=0;
			worksheet.write(rowVal,colVal,"S.No.")
			colVal = colVal + 1

			##############Header Region############################
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
			####################header stops, body starts#####################3

			for obj in unapp_user:
				obj.status= "ES"
				obj.date_mailed_on=datetime.datetime.now()
				obj.save()
			workbook.save("Files/"+bank_obj.bank+".xlsx")
			return unapp_user
#################################################
