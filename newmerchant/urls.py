from django.conf.urls import patterns, include, url
from views import reg, uploadFiles 

urlpatterns = patterns('',
    url(r'^reg/$', reg),
    url(r'^uploadfiles/$', uploadFiles),

)
