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
pprint(sys.path)

from foc.visualiser.data_organiser.complete_multigroup import CompleteMultigroupOrganiser
from foc.forecaster.common import conf

def get_data(request): 
    organiser = CompleteMultigroupOrganiser()
    repr = organiser.get_representation(conf)
    countries = organiser._extractor.get_countries()
#    if request.is_ajax():
#        indicator = countries[0].get_indicator("SL.AGR.EMPL.ZS")
#        i=randint(0,len(indicator.get_dates())-1)
#        date = indicator.get_dates()[i]
#        data = {
#            'x': date,
#            'y': indicator.get_value_at(date)
#        } 
    #if request.is_ajax():
    return HttpResponse(simplejson.dumps(repr), mimetype="application/json")
        
    #return HttpResponse(simplejson.dumps(data), mimetype="application/json")
