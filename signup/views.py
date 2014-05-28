from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import staticfiles
import datetime, hashlib, json,os, random
from django.http import HttpResponse, Http404
from hashlib import sha1
import hmac
import binascii
from models import *

def reg(request):
    if request.method == 'GET':
        category_list = CompanyCategory.objects.values_list('category', flat=True).distinct()
        business_list = BusinessType.objects.values_list('type', flat=True).distinct()
        service_list = Service.objects.values()
        return render_to_response("index.html", {'categories':category_list,'businesstypes':business_list, 'services':service_list})
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
                response_data = {}
                response_data['status'] = 'success'
                response_data['step'] = 1
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
        key = "d24c6ba5e15fb1c7e30f7bffe07c3b75aa99b635"
        merchantTxnId = ''.join(random.choice('0123456789ABCDEFGHIJ') for i in range(32))
        merchantId = "1234"
        orderAmount = sum(charges)
        currency = 'INR'
        data=merchantId+str(orderAmount)+merchantTxnId+currency
        hashed = hmac.new(key, data, sha1)
        returndata = {'secSignature': binascii.b2a_hex(hashed.digest())[:-1],'currency':'INR','orderAmount':orderAmount,'merchantTxnId':merchantTxnId, 'merchantId':merchantId, 'merchantEmail': merchantEmail,'companyName':companyName};
        return HttpResponse(json.dumps(returndata), content_type="application/json")
    else:
        raise Http404
