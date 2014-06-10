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
                    return render_to_response("index.html", {'step':0,'dashboardbody':'Nothing to do here<br>until you pay us first by<a href="../2">clicking here</a>'})
                if step==4 or step==3:
                    temphtml='<table style="border-bottom:2px solid rgb(240,240,240);left: 36%;position: relative;"><tr><td style="text-align:center"><strong>Bank</strong></td><td style="text-align:center"><strong>Status</strong></td></tr>'
                    banks = MerchantBankApproval.objects.filter(merchant=merchant)
                    for elem in banks:
                        if elem.status == 'A':
                            temphtml += '<tr><td class="bank-name">'+elem.bank.bank+'</td><td class="approved-status" style="color:green"><i class="fa fa-check-square fa-1x"></i>Approved</td></tr>'
                        elif elem.status == 'P':
                            temphtml += '<tr><td class="bank-name">'+elem.bank.bank+'<td class="pending-status" style="color:rgb(200,200,200)"><i class="fa fa-exclamation-circle fa-1x"></i>Pending</td></tr>'
                    filelist = os.listdir('./files/'+ merchant.user.email + '/')
                    no_file_uploaded = len(set([elem[:4] for elem in filelist]))
                    total = 10
                    temphtml += '<br><br><tr><td style="text-align:center"><strong>No. of Docs Left</strong></td><td style="text-align:center"><strong>'+str(total-no_file_uploaded)+ '/' +str(total) +'</strong></td></tr></table>'
                    return render_to_response("index.html", {'step':0,'dashboardbody':temphtml})

            elif step==2:
                servicelist =  MerchantService.objects.filter(merchant=merchant)
                charges = [a.service.charges for a in servicelist]
                return render_to_response('index.html', {'step':step,'amt':sum(charges)})
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
            elif req_step=='3':
                return render_to_response('index.html', {'step':3})
            elif req_step=='4':
                return render_to_response('index.html', {'step':4})
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
                return render_to_response("index.html", {'step':0,'dashboardbody':'Nothing to do here<br>get started with signup by <a href="../1">clicking here</a>'})
                
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
            merchant = Merchant(user=user, name=name, phone=phone, url=url)
            merchant.save() 
            category = CompanyCategory.objects.get(category=company_category)
            btype = BusinessType.objects.get(type=business_type)
            company = Company(name=company_name,merchant=merchant, company_category=category, business_type = btype)
            company.save()
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
            if not os.path.exists('./files/'+request.user.email):
                os.makedirs('./files/'+ request.user.email)
            if not os.path.exists('./files/'+ request.user.email + '/' + request.FILES.keys()[0]):
                os.makedirs('./files/'+ request.user.email + '/' + request.FILES.keys()[0])
            path = './files/'+ request.user.email + '/' + request.FILES.keys()[0] + '/' + request.FILES[request.FILES.keys()[0]].name
            f = request.FILES[request.FILES.keys()[0]]   
            destination = open(path, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
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
        merchant.step = 3
        merchant.save()
        banks = Bank.objects.all()
        for elem in banks:
            merchant_bank = MerchantBankApproval(merchant=merchant, bank=elem, status='P', remarks='')
            merchant_bank.save()
        if not os.path.exists('./files/'+request.user.email):
            os.makedirs('./files/'+ request.user.email)
    return HttpResponseRedirect('../reg/3')

