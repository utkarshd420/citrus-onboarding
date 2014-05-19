from django.conf.urls import patterns, include, url
from views import check, new, upload, uploadFiles 

urlpatterns = patterns('',
    url(r'^check/$', check),
    url(r'^new/$', new),
    url(r'^upload_file/$', upload),
    url(r'^uploadfiles/$', uploadFiles),

)
