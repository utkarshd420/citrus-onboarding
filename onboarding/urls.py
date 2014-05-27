from django.conf.urls import patterns, include, url
#from signup.views import check
from django.contrib import admin
admin.autodiscover()
urlpatterns = [
    # Examples:
    # url(r'^$', 'onboarding.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^new/', include('signup.urls')),


]
