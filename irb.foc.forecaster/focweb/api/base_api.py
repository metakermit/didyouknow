'''
Created on Jun 28, 2012

@author: Matija
'''

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
import datetime
from django.utils import simplejson
import time
from random import randint