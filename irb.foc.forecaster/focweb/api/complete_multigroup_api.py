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
from foc.visualiser.data_organiser.scatter_matrix import ScatterMatrixOrganiser
from foc.forecaster.common import conf

def get_data(request): 
    organiser = CompleteMultigroupOrganiser()
    
    if request.is_ajax():
        if 'countries[]' in request.GET and 'indicators[]' in request.GET: # We should check that we got exactly two indicators!
            countries = request.GET.getlist('countries[]')
            indicators = request.GET.getlist('indicators[]')
            conf.countries = countries 
            conf.indicators = indicators 
            representation = organiser.get_representation(conf)
            print("representation is:")
            print(representation)
        # If no countries are required return empty json.
        else:
            representation = []
    # For fetching json from /getdata/ url directly.
    else:
        conf.countries = ["HRV","USA"]
        representation = organiser.get_representation(conf)

    return HttpResponse(simplejson.dumps(representation), mimetype="application/json")


def get_data_scatter(request): 
    organiser = ScatterMatrixOrganiser()
    
    if request.is_ajax():
        if 'countries[]' in request.GET and 'indicators[]' in request.GET: # We should check that we got exactly two indicators!
            countries = request.GET.getlist('countries[]')
            indicators = request.GET.getlist('indicators[]')
            conf.countries = countries 
            conf.indicators = indicators 
            representation = organiser.get_representation(conf)
            print("representation is:")
            print(representation)
        # If no countries are required return empty json.
        else:
            representation = []
    # For fetching json from /getdata/ url directly.
    else:
        conf.countries = ["HRV","USA"]
        representation = organiser.get_representation(conf)

    return HttpResponse(simplejson.dumps(representation), mimetype="application/json")
