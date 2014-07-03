from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import staticfiles
import datetime, hashlib, json,os, random
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from hashlib import sha1
import hmac
import binascii
from models import *

@csrf_exempt
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
                    if merchant.verified_account==False:
                        formhtml = "<span style='text:align:center'><form method='post' action='../../verify/'>Please Verify the Amount that we have submitted  before proceeding: <input id='veramt' name='veramt'  type='text' style='width:40px'/>&nbsp;&nbsp;<input class='btn btn-primary ' style='margin-bottom:10px' value='Verify' type='submit'/></form></span>"
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
            elif merchant.verified_account==False:
                formhtml = "<form method='post' action='../../verify/'>Please Verify the Amount that we have submitted  before proceeding: <input id='veramt' name='veramt'  type='text' style='width:40px'/>&nbsp;&nbsp;<input class='btn btn-primary ' style='margin-bottom:10px' value='Verify' type='submit'/></form>"
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
    txn = Txn.objects.get(merchant=merchant)
    print "ver amt1 is %s" %(txn.verification_amount)
    print "ver amt2 is %s" %(request.POST.get('veramt'))
    if(str(txn.verification_amount) == str(request.POST.get('veramt'))):
        merchant.verified_account = True
        merchant.save()
    print merchant.verified_account
    return HttpResponseRedirect('../reg/0/')
