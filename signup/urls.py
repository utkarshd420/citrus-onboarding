from django.conf.urls import patterns, include, url
from views import reg, upload_files, gen_hmac

urlpatterns = patterns('',
    url(r'^reg/$', reg),
    url(r'^uploadfiles/$', upload_files),
    url(r'^gencode/$', gen_hmac),

)
