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
            representation = organiser.get_representation(conf)
            print("representation is:")
            print(representation)
        # If no countries are recquired return empty json.
        else:
            representation = []
    # For fetching json from /getdata/ url directly.
    else:
        conf.countries = ["HRV"]
        representation = organiser.get_representation(conf)

    return HttpResponse(simplejson.dumps(representation), mimetype="application/json")
