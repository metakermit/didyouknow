'''
Created on Jun 28, 2012

@author: Matija
'''

from base_api import *
import sys
from pprint import pprint
pprint(sys.path)

from foc.visualiser.data_organiser.complete_multigroup import CompleteMultigroupOrganiser
from foc.forecaster.common import conf

def get_data(request): 
    organiser = CompleteMultigroupOrganiser()
    repr = organiser.get_representation(conf)
    countries = organiser._extractor.get_countries()
    if request.is_ajax():
        indicator = countries[0].get_indicator("SL.AGR.EMPL.ZS")
        i=randint(0,len(indicator.get_dates())-1)
        date = indicator.get_dates()[i]
        data = {
            'x': date,
            'y': indicator.get_value_at(date)
        } 
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        
    #return HttpResponse(simplejson.dumps(data), mimetype="application/json")
