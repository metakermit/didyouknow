from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
import datetime
from django.utils import simplejson
import time
from random import randint

def hello(request):
    return HttpResponse("Hello world")

def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html', {'current_date': now})

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    #assert False
    #html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    #return HttpResponse(html)
    return render_to_response('hours_ahead.html', {'hour_offset': offset, 'next_time': dt})

def display_meta(request):
    values = request.META.items()
    values.sort()
    #html = []
    #for k, v in values:
    #    html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    #return HttpResponse('<table>%s</table>' % '\n'.join(html))
    return render_to_response('display_meta.html', {'values': values})

def highcharts(request, number):
    return render_to_response('highcharts_example' + number + '.html')

def superformula(request):
    return render_to_response('superformula.html')

def get_data(request):
    if request.is_ajax():
        data = {
            'x': round(time.time()*1000),
            'y': round(randint(0,100))
        }
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def live_server_data(request):
    return render_to_response('highcharts_live_server_data.html')



