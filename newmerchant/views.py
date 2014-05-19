from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib import staticfiles
import datetime, hashlib
from django.http import HttpResponse

@csrf_exempt
def new(request):
  print request.POST
  passwd= request.POST.get('password')
  username =hashlib.md5(request.POST.get('email')).hexdigest()[:30] 
  user = User.objects.create_user(hashlib.md5(request.POST.get('email')).hexdigest()[:30], request.POST.get('email'), request.POST.get('password'))
  user.save()
  user.new.company_name = request.POST.get('company-name')
  user.new.company_category = request.POST.get('company-category')
  user.new.name = request.POST.get('your-name')
  user.new.phone = request.POST.get('phone')
  user.new.reg_date = datetime.datetime.now()
  user.new.step = 1
  user.new.save()
  user = authenticate(username=hashlib.md5(request.POST.get('email')).hexdigest()[:30], password=passwd)
  login(request, user)
  if user is not None:
    html = "<html><body>"+username +", "+ passwd +"</body></html>"
    return HttpResponse(html)
  else:
    html = "<html><body>not done</body></html>"
    #return HttpResponse(html)
def check(request):
  if request.user.is_authenticated():
    return render(request, "index.html")
    return HttpResponse(str(request.user.email))
def uploadFiles(request):
  if request.user.is_authenticated():
    return render(request, "documents.html")
    return HttpResponse(str(request.user.email))
@csrf_exempt
def upload(request):
  print "hola"
  print request.FILES.keys()[0]
#  return HttpResponse(str(request.user.username))
#  id = request.POST['id']
  path = './'+ request.user.email + "__" +request.FILES.keys()[0]
  f = request.FILES[request.FILES.keys()[0]]   
  destination = open(path, 'wb+')
  for chunk in f.chunks():
    destination.write(chunk)
  destination.close()
  return HttpResponse(str(request.user.username))

