'''
Created on Jun 28, 2012

@author: Matija
'''

#from base_api import *
# redundant
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
import datetime
from django.utils import simplejson
import time
from random import randint
# ----------
import sys
from pprint import pprint
#pprint(sys.path)

from foc.visualiser.data_organiser.complete_multigroup import CompleteMultigroupOrganiser
from foc.forecaster.common import conf

def get_data(request): 
    organiser = CompleteMultigroupOrganiser()
    
    
    if request.is_ajax():
        if 'countries[]' in request.GET:
            countries = request.GET.getlist('countries[]')
            conf.countries = countries 
            repr = organiser.get_representation(conf)
            print("repr is:")
            print(repr)
        # If no countries are recquired return empty json.
        else:
            repr = []
    # For fetching json from /getdata/ url directly.
    else:
        conf.countries = ["HRV"]
        repr = organiser.get_representation(conf)

    return HttpResponse(simplejson.dumps(repr), mimetype="application/json")
