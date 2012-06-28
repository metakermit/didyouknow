#from django.http import HttpResponse, Http404

#import sys
#from pprint import pprint

#pprint(sys.path)

from django.shortcuts import render_to_response
from foc.forecaster.sources.extractor import Extractor
from foc.forecaster.common import conf

def hello(request):
    extractor = Extractor()
    countries = extractor.fetch_data_per_conf(conf)
    return render_to_response('index.html', {'countries': countries})



