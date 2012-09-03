from django.conf.urls import patterns, include, url
from django.contrib import admin
from django_example.views import hello, current_datetime, hours_ahead, display_meta, highcharts, superformula, live_server_data, get_data
from books import views

# This should come here (not after urlpatterns!)
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_example.views.home', name='home'),
    # url(r'^django_example/', include('django_example.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    ('^hello/$', hello),
    (r'^time/$', current_datetime),
    (r'^time/plus/(\d{1,2})/$', hours_ahead),
    (r'^meta/$', display_meta),
    #(r'^search-form/$', views.search_form),
    (r'^search/$', views.search),
    (r'^highcharts(\d)/$', highcharts),
    (r'^superformula/$', superformula),
    (r'^live/$', live_server_data),
    (r'^getdata/$', get_data),
)

