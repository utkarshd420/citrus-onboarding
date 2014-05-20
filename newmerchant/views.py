from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import staticfiles
import datetime, hashlib, json
from django.http import HttpResponse

def reg(request):
  if request.method == 'GET':
    return render(request, "index.html")
  else:
    try:
      passwd= request.POST.get('password')
      username =hashlib.md5(request.POST.get('email')).hexdigest()[:30] 
      user = User.objects.create_user(hashlib.md5(username).hexdigest()[:30], username, passwd)
      user.save()
      user.new.company_name = request.POST.get('company-name')
      user.new.company_category = request.POST.get('company-category')
      user.new.name = request.POST.get('your-name')
      user.new.phone = request.POST.get('phone')
      user.new.reg_date = datetime.datetime.now()
      user.new.step = 1
      user.new.save()
      user = authenticate(username=hashlib.md5(username).hexdigest()[:30], password=passwd)
      login(request, user)
      if user is not None:
        response_data = {}
        response_data['status'] = 'success'
        response_data['step'] = 1
        return HttpResponse(json.dumps(response_data), content_type="application/json")
      else:
        response_data = {}
        response_data['status'] = 'failed'
        response_data['step'] = 0 
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    except Exception as e:
      response_data = {}
      response_data['status'] = 'failed'
      response_data['step'] = 0 
      response_data['msg'] = str(e) 
      return HttpResponse(json.dumps(response_data), content_type="application/json")
      
def uploadFiles(request):
  if request.method == 'GET':
    if request.user.is_authenticated():
      return render(request, "documents.html")
    else:
      return HttpResponse("Failed")
  else:
    if request.user.is_authenticated():
      path = './'+ request.user.email + "__" +request.FILES.keys()[0]
      f = request.FILES[request.FILES.keys()[0]]   
      destination = open(path, 'wb+')
      for chunk in f.chunks():
        destination.write(chunk)
      destination.close()
      return HttpResponse(str(request.user.username))
    else:
      return HttpResponse("Failed")

