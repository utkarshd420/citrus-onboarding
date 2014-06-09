from django.conf.urls import patterns, include, url
from views import reg, upload_files, gen_hmac, citrusresponse

urlpatterns = patterns('',
    url(r'^reg/(?P<step>\w+)/$', reg),
    url(r'^uploadfiles/$', upload_files),
    url(r'^gencode/$', gen_hmac),
    url(r'^citrusresponse/$', citrusresponse),

)
