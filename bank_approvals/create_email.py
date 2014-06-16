import xlwt,os
from datetime import datetime
def create_workbook(bank_obj,choiceList):
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
	####################header stops, body starts#####################
	dirname=str(datetime.now().strftime('%Y.%m.%d'))
	if not os.path.exists('./'+dirname+'/'):
		os.makedirs("%s"%dirname)

	workbook.save(dirname+"/"+bank_obj.bank+".xlsx")
	return dirname