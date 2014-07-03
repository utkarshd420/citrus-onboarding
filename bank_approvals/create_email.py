from django.db import models
from signup.models import *
import xlwt,os,xlsxwriter,string
from datetime import datetime
def create_workbook(bank_obj,choiceList,unapp_user):
	workbook = xlwt.Workbook();
	worksheet = workbook.add_sheet(bank_obj.bank)
	rowVal=0;colVal=0;status_list_val = 0;
	style_string = """font:bold on;
					  border:left thick,top thick,bottom thick,right thick;
					  alignment:horizontal center,vertical center;
					  pattern:pattern solid,fore_color gray25"""
	header_style = xlwt.easyxf(style_string)

	worksheet.write(rowVal,colVal,"S.No.",style=header_style)
	for user in unapp_user:
		rowVal = rowVal+1
		worksheet.write(rowVal,colVal,rowVal)
	colVal = colVal+1
	rowVal = 0
	##############Header Region############################


	# Check for empty strings #


	if (choiceList.merchant_name == True):
		worksheet.write(rowVal,colVal,"Merchant Name",style=header_style)
		for user in unapp_user:
			rowVal = rowVal+1
			worksheet.write(rowVal,colVal,user.company.name)
			worksheet.col(colVal).width = 100*100
		colVal = colVal+1
		rowVal = 0
	if (choiceList.merchant_friendly_name == True):
		worksheet.write(rowVal,colVal,"Merchant Friendly Name",style=header_style)
		for user in unapp_user:
			rowVal = rowVal+1
			worksheet.write(rowVal,colVal,user.company.friendly_name)
			worksheet.col(colVal).width = 100*100
		colVal = colVal+1
		rowVal = 0

	if (choiceList.merchant_url == True):
		worksheet.write(rowVal,colVal,"Merchant Website",style=header_style)
		for user in unapp_user:
			rowVal = rowVal+1
			worksheet.write(rowVal,colVal,user.company.merchant.url)
			worksheet.col(colVal).width = 100*100
		rowVal = 0
		colVal = colVal+1
	if (choiceList.merchant_region == True):
		worksheet.write(rowVal,colVal,"Merchant Region",style=header_style)
		worksheet.col(colVal).width = 100*100
		colVal = colVal+1
	if (choiceList.merchant_category == True):
		worksheet.write(rowVal,colVal,"Merchant Category",style=header_style)
		worksheet.col(colVal).width = 100*100
		for user in unapp_user:
			rowVal = rowVal+1
			worksheet.write(rowVal,colVal,str(user.company.company_category))
		rowVal = 0
		colVal = colVal+1
	if (choiceList.merchant_commercial == True):
		worksheet.write(rowVal,colVal,"Merchant Commercials",style=header_style)
		for user in unapp_user:
			temp = merchant_commercial.objects.get(company=user.company)
			write_obj = commercial.objects.get(merchant_commercial=temp,bank=bank_obj)
			rowVal = rowVal+1
			if(write_obj.mode == "INR"):
				worksheet.write(rowVal,colVal,str(write_obj.commercial_value)+" Rs. ")
			else:
				worksheet.write(rowVal,colVal,str(write_obj.commercial_value)+" % ")
		worksheet.col(colVal).width = 100*55
		rowVal = 0
		colVal = colVal+1
	if (choiceList.merchant_type == True):
		worksheet.write(rowVal,colVal,"Merchant Type",style=header_style)
		for user in unapp_user:
			rowVal = rowVal+1
			worksheet.write(rowVal,colVal,str(user.company.business_type))
		rowVal = 0
		worksheet.col(colVal).width = 100*100
		colVal = colVal+1
	if (choiceList.merchant_address == True):
		worksheet.write(rowVal,colVal,"Merchant Address",style=header_style)
		colVal = colVal+1
		worksheet.col(colVal).width = 100*100
	if (choiceList.bank_share == True):
		worksheet.write(rowVal,colVal,"Bank Share",style=header_style)
		for user in unapp_user:
			temp = bank_commercial.objects.get(bank=bank_obj,company_category= user.company.company_category)
			write_obj = bank_commercial_value.objects.filter(bank_commercial=temp)
			merchant_temp = merchant_commercial.objects.get(company=user.company)
			merchant_commercial_obj = commercial.objects.get(merchant_commercial=merchant_temp,bank=bank_obj)
			max_val = 0;mode = " % ";flag=0;
			for obj in write_obj:
				if(obj.from_merchant == True):
					if((merchant_commercial_obj.commercial_value * obj.value )/100 >max_val):
						flag=1
						temp_bank_commercial_obj = obj
						max_val = (merchant_commercial_obj.commercial_value * obj.value )/100
						if(obj.mode == "INR"):
							mode = " Rs. "
						else:
							mode = " % "
						if(merchant_commercial_obj.mode == "INR"):
							mode = " Rs. "

				else:
					if (obj.value > max_val):
						flag = 0
						max_val = obj.value
						if(obj.mode == "INR"):
							mode = " Rs. "
						else:
							mode = " % "
						if(merchant_commercial_obj.mode == "INR"):
							mode = " Rs. "
			rowVal = rowVal+1
			if (flag==1):
				worksheet.write(rowVal,colVal,"%s %s of Citrus Commercial"%(temp_bank_commercial_obj.value," % "))
			if (flag==0):
				worksheet.write(rowVal,colVal,str(max_val)+mode)
		worksheet.col(colVal).width = 100*50
		rowVal = 0
		colVal = colVal+1
	if (choiceList.bank_code == True):
		worksheet.write(rowVal,colVal,"Bank Code",style=header_style)
		colVal = colVal+1
	if (choiceList.expected_no_txn == True):
		worksheet.write(rowVal,colVal,"Expected no. of Txn",style=header_style)
		for user in unapp_user:
			rowVal = rowVal+1
			worksheet.write(rowVal,colVal,"50,000")
		rowVal = 0
		worksheet.col(colVal).width = 100*50
		colVal = colVal+1
	if (choiceList.expected_no_vol == True):
		worksheet.write(rowVal,colVal,"Expected No. of Volume",style=header_style)
		worksheet.col(colVal).width = 100*55
		colVal = colVal+1
	if (choiceList.requested_date == True):
		worksheet.write(rowVal,colVal,"Requested Date",style=header_style)
		for user in unapp_user:
			rowVal = rowVal+1
			worksheet.write(rowVal,colVal,str(datetime.now().strftime('%d.%m.%Y')))
		rowVal = 0
		worksheet.col(colVal).width = 100*50
		colVal = colVal+1
	if (choiceList.status == True):
		worksheet.write(rowVal,colVal,"Status",style=header_style)
		status_list_val = colVal
		colVal = colVal+1
	if (choiceList.remarks == True):
		worksheet.write(rowVal,colVal,"Remarks",style=header_style)
		colVal = colVal+1
	colVal=0
	rowVal= rowVal +1
	####################header stops#####################
	dirname=str(datetime.now().strftime('%Y.%m.%d'))
	if not os.path.exists('./'+dirname+'/'):
		os.makedirs("%s"%dirname)

	workbook.save(dirname+"/"+bank_obj.bank+".xls")
	## making a status field as dropdown ##
	
	return dirname