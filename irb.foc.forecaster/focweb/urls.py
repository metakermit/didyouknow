from django.conf.urls import patterns, include, url
from views import foc, multiselect, d3
from api.complete_multigroup_api import get_data

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_app.views.home', name='home'),
    # url(r'^django_app/', include('django_app.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    url(r'^foc/', foc),
    url(r'^getdata/', get_data),
    
    url(r'^multiselect/', multiselect),
    url(r'^d3/', d3),
)
