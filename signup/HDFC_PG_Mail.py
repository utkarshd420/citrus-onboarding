import xlwt, xlrd
import xlsxwriter
from xlutils.copy import copy
from signup.models import *

def create_hdfc_pg_sheet(merchant_obj):

	workbook = xlrd.open_workbook('MasterTemplate.xls')
	sheet = workbook.sheet_by_name('Checklist')

	wb = copy(workbook)
	w_sheet = wb.get_sheet(0)




	style_string = """font:bold on;
						  border:left thick,top thick,bottom thick,right thick;
						  alignment:horizontal center,vertical center;
						  """
	header_style = xlwt.easyxf(style_string)

	w_sheet.col(0).width = 256 * 5
	# set width.. 256 = 1 width of 0 character

	w_sheet.col(1).width = 256 * 5
	# set width.. 256 = 1 width of 0 character
	
	w_sheet.col(2).width = 256 * 60
	# set width.. 256 = 1 width of 0 character

	w_sheet.col(3).width = 256 * 40
	# set width.. 256 = 1 width of 0 character
	
	w_sheet.col(4).width = 256 * 20
	# set width.. 256 = 1 width of 0 character

	a = Company.objects.filter(merchant=merchant_obj)[0]
	x = additional_company_details.objects.filter(merchant=merchant_obj)[0]
	#b = merchant_contact_details.objects.filter(merchant=merchant_obj)[0]
	l = merchant_website_details.objects.filter(merchant=merchant_obj)[0]
	c = l.website_details

	w_sheet.write(9,3,'CITRUS PAY - %s'%(a.name))

	w_sheet.write(11,3,'%s'%(x.address.flat_no))
	w_sheet.write(12,3, '%s'%(x.address.building_name)) # row, column, value
	w_sheet.write(13,3,'%s'%(x.address.street_name))
	w_sheet.write(14,3,'%s'%(x.address.road_name))
	w_sheet.write(15,3,'%s'%(x.address.area_name))
	w_sheet.write(16,3,'%s'%(x.address.city))
	w_sheet.write(17,3,'%s'%(x.address.state))

	#w_sheet.write(19,3,'%s'%(b.operation_contact.name))
	#w_sheet.write(20,3,'%s'%(b.operation_contact.contact_number))

	w_sheet.write(23,3,'%s'%(a.company_category))
	w_sheet.write(24,3,'Full')
	
	#url= str(merchant_obj.merchant.url)
	#w_sheet.write(28,3,'%s'%(url))
	w_sheet.write(28, 3, xlwt.Formula('HYPERLINK("'+merchant_obj.merchant.url+'"; "'+merchant_obj.merchant.url+'")'))

	w_sheet.write(30,3,'%s'%(x.date_of_establishment))

	w_sheet.write(31,3,'NO')
	w_sheet.write(34, 3, xlwt.Formula('HYPERLINK("'+merchant_obj.merchant.url+'"; "'+merchant_obj.merchant.url+'")'))

	w_sheet.write(52,3,'%s'%(x.company_turnover))

	w_sheet.write(53,3,'%s'%(x.avg_monthly_volume))

	w_sheet.write(63, 3, xlwt.Formula('HYPERLINK("'+c.privacy_policy_url+'"; "'+c.privacy_policy_url+'")'))
	w_sheet.write(64, 3, xlwt.Formula('HYPERLINK("'+c.returns_refund_url+'"; "'+c.returns_refund_url+'")'))
	w_sheet.write(65, 3, xlwt.Formula('HYPERLINK("'+c.terms_conditions_url+'"; "'+c.terms_conditions_url+'")'))
	w_sheet.write(66, 3, xlwt.Formula('HYPERLINK("'+c.prduct_description_url+'"; "'+c.product_description_url+'")'))
	w_sheet.write(67, 3, xlwt.Formula('HYPERLINK("'+c.prduct_description_url+'"; "'+c.product_description_url+'")'))
	w_sheet.write(68, 3, xlwt.Formula('HYPERLINK("'+c.about_us_url+'"; "'+c.about_us_url+'")'))
	w_sheet.write(69, 3, xlwt.Formula('HYPERLINK("'+c.shipping_delivery_url+'"; "'+c.shipping_delivery_url+'")'))
	w_sheet.write(70, 3, xlwt.Formula('HYPERLINK("'+c.contact_us_url+'"; "'+c.contact_us_url+'")'))
	w_sheet.write(71, 3, xlwt.Formula('HYPERLINK("'+c.disclaimer_url+'"; "'+c.disclaimer_url+'")'))
	


	w_sheet.write(16, 3, xlwt.Formula('HYPERLINK("http://yujitomita.com"; "click me")'))

	dirname='HDFC_PG_'+str(datetime.now().strftime('%Y.%m.%d'))
	if not os.path.exists('./'+dirname+'/'):
		os.makedirs("%s"%dirname)

	wb.save(dirname+"/"+merchant_obj.merchant.name+".xls")

	#wb.save('HDFC_PG_%s'%(merchant_obj.merchant.name)+'.xls')

	# done!