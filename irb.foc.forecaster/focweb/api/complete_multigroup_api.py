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
#from subprocess import check_output, Popen, PIPE
from subprocess import Popen, PIPE # check_output is avaliable only in python 2.7!
#pprint(sys.path)

from foc.visualiser.data_organiser.complete_multigroup import CompleteMultigroupOrganiser
from foc.visualiser.data_organiser.scatter_matrix import ScatterMatrixOrganiser
#from foc.visualiser.data_organiser.rca_data import RCADataOrganiser
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
    
    # TODO: Loadin RCA data will take too long! This should be initialized before and only once!
    organiser = ScatterMatrixOrganiser()
    #organiserRCA = RCADataOrganiser()
    
    if request.is_ajax():
        #if 'countries[]' in request.GET and 'wbIndicators[]' in request.GET: # We should check that we got exactly two indicators!
        if 'countries[]' in request.GET:
            countries = request.GET.getlist('countries[]')
            wbIndicators = request.GET.getlist('wbIndicators[]')
            rcaIndicators = request.GET.getlist('rcaIndicators[]')
            conf.countries = countries 
            conf.indicators = wbIndicators 
            conf.indicators.extend(rcaIndicators)
            #conf.rcaIndicators = rcaIndicators
            representation = organiser.get_representation(conf)
            #representation = dict(representationWB.items() + representationRCA.items())
            print("representation is:")
            print(representation)
        # If no countries are required return empty json.
        else:
            representation = []
    # For fetching json from /getdata/ url directly.
    else:
        conf.countries = ["HRV","USA"]
        representationWB = organiser.get_representation(conf)

    return HttpResponse(simplejson.dumps(representation), mimetype="application/json")

def execute_sgd(request):
    
    if request.is_ajax():
        sgd = request.GET.getlist('sgd')

        fileName = "file.sgd"
        user = "#########" # HIDE USER NAME!
        
        # WINDOWS (connecting to remote Linux machine to run subgroup discovery)
        
        #proc1 = Popen(['plink',user+"@zel.lis.lo","cat > /home/"+user+"/sgd/working/" + fileName], stdout=PIPE, stdin=PIPE, universal_newlines=True)
        #proc1.stdin.write(sgd[0])

        #proc2 = Popen(['plink',user+"@zel.lis.lo","cd /home/"+user+"/sgd/working/; /home/"+user+"/sgd/working/execute_sgd " + fileName + " true"])
        #proc2.communicate()

        #proc3 = Popen(['plink',user+"@zel.lis.lo","cat /home/"+user+"/sgd/working/" + fileName + ".rr"], stdout=PIPE, stdin=PIPE, universal_newlines=True)
        #output = proc3.communicate()[0]
        
        
        # LINUX (running subgroup discovery locally)
        
        f1 = open("./sgd/working/" + fileName,"w")
        f1.write(sgd[0])
        f1.close()
 
        proc = Popen(["cd ./sgd/working/; ./execute_sgd " + fileName + " true"],shell=True)
        proc.communicate()
        
        f2 = open("./sgd/working/" + fileName + ".rr","r")
        output = f2.read()
        f2.close()

    else:
        pass
    
    # check_output is available from Python 2.7!
    #output = check_output('python -c \"print 4*5\"',shell=True)
    #output = "(crisis=true) (gdp<=-0.342) asd asd (trunk>0.34545)"
    #output = check_output('pwd',shell=True)
    
    return HttpResponse(output, mimetype="text/plain; charset=utf-8")
    
