from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import staticfiles
import datetime, hashlib, json,os, random
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from hashlib import sha1
import hmac
import binascii
from models import *

@csrf_exempt
def login_user(request):
    if request.method == 'GET':
        return render_to_response("login.html")
    else:
        username = hashlib.md5(request.POST.get('email')).hexdigest()[:30] 
        password = request.POST.get('passwd')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("../reg/0/")
            else:
                return render_to_response("login.html",{errormsg:"User Not active"})
        else:
            return render_to_response("login.html",{'errormsg':"User Login invalid"})
def logout_user(request):
    logout(request)
    return HttpResponseRedirect("../login/")
def reg(request, **kwargs):
    if request.method == 'GET':
        req_step = kwargs.get('step')
        print req_step
        if request.user.is_authenticated():
            username = request.user.username
            merchant = Merchant.objects.get(user__username=username)
            step = merchant.step
            if req_step=='0':
                if step==2:
                    return render_to_response("index.html", {'step':0,'dashboardbody':'<span style="text-align:center;position:relative;left:36%">Nothing to do here until you pay us first by<a href="../2">clicking here</a></span>'})

                elif step==4 or step==3:
                    if merchant.verified_account==False and merchant_bank_details.objects.filter(merchant=merchant):
                        formhtml = "<span style='text-align:center;position:relative;'><form method='post' action='../../verify/'>Please Verify the Amount that we have submitted  before proceeding: <input id='veramt' name='veramt'  type='text' style='width:40px'/>&nbsp;&nbsp;<input class='btn btn-primary ' style='margin-bottom:10px' value='Verify' type='submit'/></form></span>"
                        return render_to_response("index.html",{'step':0,'dashboardbody':formhtml})
                    elif(not merchant_bank_details.objects.filter(merchant=merchant)):
                        formhtml = "<span style='text-align:center;position:relative;left:36%'><a href='../../additional/'>Click Here</a> to fill in additional details</span>"
                        return render_to_response("index.html",{'step':0,'dashboardbody':formhtml})
                    temphtml='<table style="border-bottom:2px solid rgb(240,240,240);left: 36%;position: relative;"><tr><td style="text-align:center"><strong>Bank</strong></td><td style="text-align:center"><strong>Status</strong></td></tr>'
                    company = Company.objects.get(merchant= merchant)
                    banks = MerchantBankApproval.objects.filter(company=company)
                    for elem in banks:
                        if elem.status == 'A':
                            temphtml += '<tr><td class="bank-name">'+elem.bank.bank+'</td><td class="approved-status" style="color:green"><i class="fa fa-check-square fa-1x"></i>Approved</td></tr>'
                        elif elem.status == 'P':
                            temphtml += '<tr><td class="bank-name">'+elem.bank.bank+'<td class="pending-status" style="color:rgb(200,200,200)"><i class="fa fa-exclamation-circle fa-1x"></i>&nbsp;Pending</td></tr>'
                    no_file_uploaded = 0
                    if os.path.exists('./files/'+ merchant.user.email + '/'):
                        filelist = os.listdir('./files/'+ merchant.user.email + '/')
                        no_file_uploaded = len(set([elem[:4] for elem in filelist]))
                    total = 10
                    temphtml += '<br><br><tr><td style="text-align:center"><strong>No. of Docs Left</strong></td><td style="text-align:center"><strong>'+str(total-no_file_uploaded)+ '/' +str(total) +'</strong></td></tr></table>'
                    return render_to_response("index.html", {'step':0,'dashboardbody':temphtml})
            
            elif req_step=='2':
                print "hakuna matata"
                servicelist =  MerchantService.objects.filter(merchant=merchant)
                charges = [a.service.charges for a in servicelist]
                if step>2:
                    amount = sum(charges)
                    disable = "disabled"
                    status = "Paid"
                    return render_to_response('index.html', {'step':2,'amt':amount, 'disable':disable, 'status':status})
                else:
                    amount = sum(charges)
                    disable = ""
                    status = "Pay"
                    return render_to_response('index.html', {'step':2,'amt':amount, 'disable':disable, 'status':status})
            elif req_step=='1':
                company = Company.objects.get(merchant=merchant)
                merchantservices = MerchantService.objects.filter(merchant=merchant)
                datadict = {}
                datadict['companyname'] = company.name
                datadict['companyurl'] = merchant.url
                datadict['category'] = company.company_category.category
                datadict['type'] = company.business_type.type
                datadict['name'] = merchant.name
                datadict['email'] = merchant.user.email
                datadict['phone'] = merchant.phone
                datadict['services'] = []
                a = [datadict['services'].append({'name':g.service.name, 'charges':g.service.charges}) for g in merchantservices]
                return render_to_response('indextab1.html', datadict)
            elif merchant.verified_account==False and merchant_bank_details.objects.filter(merchant=merchant):
                formhtml = "<span style='text-align:center;position:relative;'><form method='post' action='../../verify/'>Please Verify the Amount that we have submitted  before proceeding: <input id='veramt' name='veramt'  type='text' style='width:40px'/>&nbsp;&nbsp;<input class='btn btn-primary ' style='margin-bottom:10px' value='Verify' type='submit'/></form></span>"
                return render_to_response("index.html",{'step':0,'dashboardbody':formhtml})
            elif req_step=='3' and step>2:
                return render_to_response('index.html', {'step':3})
            elif req_step=='4' and step>2:
                company = Company.objects.get(merchant=merchant)
                document_list = document.objects.filter(businessType=company.business_type)
                table_html = ""
                for obj in document_list:
                    label_id = str(obj.header).replace(" ","_")
                    table_html+= '''<tr style="border-bottom:2px solid rgb(240,240,240)">
                                    <td><h4>%s</h4>
                                    <span style="color:rgb(200,200,200)">
                                    %s
                                    </span>
                                    </td>
                                    <td style="text-align:center;">
                                    <input style="display:none" type='file' id='%s'><label name="%s" onclick="$('#%s').click();"><i class="fa fa-upload fa-1x" style="padding:0.2em;"></i>Upload</label>
                                    <progress style="display:none" name="%s" max="100", value="0"></progress>
                                    </td>
                                    <td style="text-align:center;">
                                    <i class="fa fa-check-square fa-1x" style="padding:0.2em"></i>Verified
                                    </td>
                                    </tr>
                    '''%(obj.header,obj.doc_list,label_id,label_id,label_id,label_id)
                return render_to_response('index.html', {'step':4,'htmlTable':table_html})
            else:
                return HttpResponseRedirect('../0')
               
        else:
            if req_step == '1':
                print "haha"
                category_list = CompanyCategory.objects.values_list('category', flat=True).distinct()
                business_list = BusinessType.objects.values_list('type', flat=True).distinct()
                service_list = Service.objects.values()
                return render_to_response("index.html", {'categories':category_list,'businesstypes':business_list, 'services':service_list,'step':1})
            else:
                return render_to_response("index.html", {'step':0,'dashboardbody':'<span style="text-align:center;position:relative;left:36%">Nothing to do here get started with signup by <a href="../1">clicking here</a></span>'})
                
    else:
        try:
            data = json.loads(request.body).get('data')
            passwd= data.get('password')
            email  = data.get('email')
            username = hashlib.md5(email).hexdigest()[:30] 
            user = User.objects.create_user(username, email, passwd)
            user.save()
            company_name = data.get('company-name')
            company_category = data.get('company-category')
            name = data.get('your-name')
            phone = data.get('phone')
            url = data.get('company-website')
            business_type = data.get('company-business-type')
            services = data.get('services')
            reg_date = datetime.datetime.now()
            step = 1 
            merchant = Merchant(user=user, name=name, phone=phone, url=url,last_changed_on = datetime.datetime.now())
            merchant.save() 
            category = CompanyCategory.objects.get(category=company_category)
            btype = BusinessType.objects.get(type=business_type)
            company = Company(name=company_name,merchant=merchant, company_category=category, business_type = btype)
            company.save()
            documents = document.objects.filter(businessType= company.business_type)
            for doc in documents:
                document_user_status(merchant= merchant,type= doc.header).save()
            for service in services:
                serv = Service.objects.get(name=service)
                merchant_service = MerchantService(merchant=merchant, service=serv)
                merchant_service.save()
            user = authenticate(username=username, password=passwd)
            if user is not None:
                login(request, user)
                merchant.step = 2
                merchant.save()
                response_data = {}
                response_data['status'] = 'success'
                response_data['step'] = 2 
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            else:
                response_data = {}
                response_data['status'] = 'failed'
                response_data['step'] = 0 
                response_data['msg'] = 'Auth problem'
                return HttpResponse(json.dumps(response_data), content_type="application/json")
        except Exception as e:
            response_data = {}
            response_data['status'] = 'failed'
            response_data['step'] = 0 
            response_data['msg'] = str(e) 
            return HttpResponse(json.dumps(response_data), content_type="application/json")
def upload_files(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            return render(request, "documents.html")
        else:
            return HttpResponse("Failed")
    else:
        if request.user.is_authenticated():
            file_count = 1
            merchant = Merchant.objects.get(user=request.user)
            if not os.path.exists('./files/'+request.user.email):
                os.makedirs('./files/'+ request.user.email)
            if not os.path.exists('./files/'+ request.user.email + '/' + request.FILES.keys()[0]):
                os.makedirs('./files/'+ request.user.email + '/' + request.FILES.keys()[0])
            else:
                file_count = len(os.listdir('./files/'+ request.user.email + '/' + request.FILES.keys()[0]))
            file_name = request.FILES[request.FILES.keys()[0]].name
            path = './files/'+ request.user.email + '/' + request.FILES.keys()[0] + '/' + "%s%s"%("version "+str(file_count),file_name[file_name.rfind('.'):])#(request.FILES[request.FILES.keys()[0]].name)
            file_string = request.FILES.keys()[0].replace("_"," ")
            ps=document_user_status.objects.filter(merchant=merchant,type=file_string)[0]
            ps.uploaded=True
            ps.save()
            f = request.FILES[request.FILES.keys()[0]]   
            destination = open(path, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
            merchant.last_changed_on = datetime.datetime.now()
            merchant.save()
            return HttpResponse(str(request.user.username))
        else:
            return HttpResponse("Failed")
def gen_hmac(request):
    if request.method == 'GET':
        username = request.user.username
        merchant = Merchant.objects.get(user__username=username)
        merchantEmail = merchant.user.email
        company = Company.objects.get(merchant=merchant)
        companyName = company.name
        servicelist =  MerchantService.objects.filter(merchant=merchant)
        charges = [a.service.charges for a in servicelist]
        key = "8d67f4a947a6273b1aa55ef72a133d5518a9a13f"
        merchantTxnId = ''.join(random.choice('0123456789ABCDEFGHIJ') for i in range(28))
        merchantId = "mufvo8mgto"
        #orderAmount = sum(charges) 
        orderAmount = 1
        currency = 'INR'
        data=merchantId+str(orderAmount)+merchantTxnId+currency
        hashed = hmac.new(key, data, sha1)
        returndata = {'secSignature': binascii.b2a_hex(hashed.digest()),'currency':'INR','orderAmount':orderAmount,'merchantTxnId':merchantTxnId, 'merchantId':merchantId, 'merchantEmail': merchantEmail,'companyName':companyName};
        txn = Txn(merchant_tx_id=merchantTxnId,merchant=merchant,status='P',amount=orderAmount,date_time=datetime.datetime.now())
        txn.save()
        return HttpResponse(json.dumps(returndata), content_type="application/json")
    else:
        raise Http404
@csrf_exempt
def citrusresponse(request):
    print request.POST
    txn = Txn.objects.get(merchant_tx_id=request.POST.get('TxId'))
    if request.POST.get('TxStatus')=="SUCCESS":
        txn.status = 'S'
        txn.citrus_txn_id = request.POST.get('TxRefNo')
        txn.save()
        merchant = Merchant.objects.get(user__email=request.POST.get('Merchant Email'))
        print merchant
        merchant.step = 3
        merchant.last_changed_on = datetime.datetime.now()
        merchant.save()
        company = Company.objects.get(merchant = merchant)
        banks = Bank.objects.all()
        for elem in banks:
            merchant_bank = MerchantBankApproval(company=company, bank=elem, status='P', remarks='')
            merchant_bank.save()
        if not os.path.exists('./files/'+request.POST.get('Merchant Email')):
            os.makedirs('./files/'+ request.POST.get('Merchant Email'))
    return HttpResponseRedirect('../reg/3/')
@csrf_exempt
def verifyUser(request):
    print request.POST
    merchant = Merchant.objects.get(user= request.user)
    txn = Txn.objects.filter(merchant=merchant,status="S")[0]
    print "ver amt1 is %s" %(txn.verification_amount)
    print "ver amt2 is %s" %(request.POST.get('veramt'))
    if(str(txn.verification_amount) == str(request.POST.get('veramt'))):
        merchant.verified_account = True
        merchant.save()
    print merchant.verified_account
    return HttpResponseRedirect('../reg/0/')
@csrf_exempt
def additionalDetails(request):
    username = request.user.username
    merchant = Merchant.objects.get(user__username=username)
    company = Company.objects.get(merchant=merchant)
    if request.method == 'GET':
        return render_to_response('additional_details.html')
    else:
        bank_name = request.POST.get('bankName')
        branch_name = request.POST.get('branchName')
        ifsc_code = request.POST.get('ifscCode')
        account_number = request.POST.get('accNum')
        mbd = merchant_bank_details(merchant=merchant,bank_name=bank_name,branch_name=branch_name,ifsc_code=ifsc_code,account_number=account_number)
        mbd.save()
        about_us = request.POST.get('about_us_url')
        contact_us = request.POST.get('contact_us_url')
        tnc = request.POST.get('tnc_url')
        product_desc = request.POST.get('product_url')
        privacy_policy = request.POST.get('privacy_policy')
        shipping_policy = request.POST.get('shipping_policy')
        disclaimer_policy = request.POST.get('disclaimer_policy')
        merchant_website_status = request.POST.get('website_status')
        mwd = merchant_website_details(about_us_url=about_us,contact_us_url=contact_us,terms_conditions_url=tnc,product_description_url=product_desc,privacy_policy_url=privacy_policy,shipping_delivery_url=shipping_policy,disclaimer_url=disclaimer_policy,website_status=merchant_website_status)
        mwd.save()
        company.friendly_name = request.POST.get('friendly_name')
        company.save()
        date_of_incorp = request.POST.get('returns_url')
        min_ticket_size = request.POST.get('min_ticket_size')
        max_ticket_size = request.POST.get('max_ticket_size')
        monthly_vol = request.POST.get('monthly_volume')
        company_turn = request.POST.get('company_turnover')
        business_line = request.POST.get('business_line')
        international = request.POST.get('international_card')
        current_pg = request.POST.get('current_pg')
        #address
        flat_no = request.POST.get('flat_no')
        building_name  = request.POST.get('building_name')
        street_name =  request.POST.get('street_name')
        road_name =  request.POST.get('road_name')
        area_name =  request.POST.get('area_name')
        city =  request.POST.get('city')
        state =  request.POST.get('state')
        address = merchant_address(flat_no =flat_no,building_name =building_name,street_name =street_name,road_name =road_name,area_name =area_name,city =city,state =state)
        address.save()
        acd = additional_company_details(merchant=merchant,website_details=mwd,address =address,date_of_establishment =date_of_incorp,min_ticket_size =min_ticket_size,max_ticket_size =max_ticket_size,avg_monthly_volume =monthly_vol,company_turnover =company_turn,business_line =business_line,current_pg_service =current_pg,international_card_required =international)
        acd.save()
        mbcd = merchant_contact(name=request.POST.get('business_contact_name'),email=request.POST.get('business_contact_email'),contact_number=request.POST.get('business_contact_number'))
        mbcd.save()
        mocd = merchant_contact(name=request.POST.get('operational_contact_name'),email=request.POST.get('operational_contact_email'),contact_number=request.POST.get('operational_contact_number'))
        mocd.save()
        mcscd = merchant_contact(name=request.POST.get('customer_contact_name'),email=request.POST.get('customer_contact_email'),contact_number=request.POST.get('customer_contact_number'))
        mcscd.save()
        merchant_contact_details(merchant =merchant,merchant_business_contact =mbcd,merchant_operation_contact =mocd,merchant_customer_service =mcscd).save()
        return HttpResponseRedirect('../reg/0/')
