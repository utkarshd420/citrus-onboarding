from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import staticfiles
import datetime, hashlib, json,os
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
            data = json.loads(request.body)
            print data
            return HttpResponse("done")
            passwd= request.POST.get('password')
            email  = request.POST.get('email')
            username = hashlib.md5(email).hexdigest()[:30] 
            user = User.objects.create_user(username, email, passwd)
            user.save()
            user.new.company_name = request.POST.get('company-name')
            user.new.company_category = request.POST.get('company-category')
            user.new.name = request.POST.get('your-name')
            user.new.phone = request.POST.get('phone')
            user.new.reg_date = datetime.datetime.now()
            user.new.step = 1
            user.new.save()
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
        raise Http404
    elif request.method == 'POST':
        key = "d24c6ba5e15fb1c7e30f7bffe07c3b75aa99b635"
        merchantId = request.POST.get("merchantId")
        orderAmount = request.POST.get("orderAmount")
        merchantTxnId = request.POST.get("merchantTxnId")
        currency = request.POST.get("currency")
        data=merchantId+orderAmount+merchantTxnId+currency
        hashed = hmac.new(key, data, sha1)
        return HttpResponse(binascii.b2a_hex(hashed.digest())[:-1])
    else:
        raise Http404
