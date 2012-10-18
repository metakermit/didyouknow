from django.conf.urls import patterns, include, url
from views import foc, multiselect, d3, foc_d3
from api.complete_multigroup_api import get_data, get_data_scatter, execute_sgd

import dracula.local_storage.rca.api as rca_api

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

def one_time_startup():
    print rca_api._data
    pass

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_app.views.home', name='home'),
    # url(r'^django_app/', include('django_app.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    url(r'^foc/', foc),
    url(r'^focd3/', foc_d3),
    url(r'^getdata/', get_data),
    url(r'^getdatascatter/', get_data_scatter),
    
    url(r'^executesgd/', execute_sgd),
    
    url(r'^multiselect/', multiselect),
    url(r'^d3/', d3),
)

one_time_startup()