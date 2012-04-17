'''
Created on 15. 12. 2011.

@author: kermit
'''
import urllib
import urllib2
import time
# here i use json, but the api also supports xml
import json
from pprint import pprint

from forecaster.model.indicator import Indicator


def make_request(query):
    attempts = 3
    sucess = False
    while attempts>0 and sucess!=True:
        try:
            # do the actual query
            http_response = urllib2.urlopen(query)
            # and if an exception wasn't thrown we did it!
            sucess = True
        except urllib2.HTTPError, e:
            print "World Bank server error, giving it another try."
            # let the World Bank cool down a bit :)
            time.sleep(10)
            # that was one unsuccessful attempt
            attempts-=1
            if attempts == 0:
                # OK, we won't try any more
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
                print('Reason: ', e.reason)
                raise
    data = json.load(http_response)
    return data

def parse_single_country(data_list):
    values=[]
    dates=[]
    for entity in data_list:
        try:
            value = float(entity["value"])
            date = int(entity["date"])
        except TypeError: # value wasn't a float 
            pass
        else:
            values.append(value)
            dates.append(date)
    #pprint(dates)
    #pprint(values)
    indicator = Indicator(dates, values)
    return indicator

def abstract_query(parameters):
    read_pages=0
    total_pages=1
    # build url request
    root = 'http://api.worldbank.org'
    url = root + parameters
    #example url:
    #'http://api.worldbank.org/countries/hrv/indicators/SP.POP.TOTL'
    #'http://api.worldbank.org/countries/all/indicators/SP.POP.TOTL?date=2000:2001'
    data_list = [] # we store the responses here
    while(read_pages<total_pages):
        try:
            # query results from the current page
            query = url + '&' + str(read_pages+1)
            response = make_request(query)
        except urllib2.HTTPError:
            #error_msg = "Was fetching indicator %s for country %s between %s and %s."
            #print error_msg % (indicator, country, start_date, end_date)
            print "The query was:\n" + query + "\n" 
            raise
        
        # btw response[0] is the information on the pages etc,
        # actual data is in a list at index 1
        # sort list by date
        response[1].sort(key = lambda element : element['date'])
        # and add the items from this page to the main list 
        data_list.extend(response[1])
        total_pages = response[0]['pages']
        read_pages = read_pages + 1
    # response[1] contains a list of dictionaries - one dic per year
    #pprint(data_list)
    # check to see if all of the http_response is loaded
    assert(response[0]['total']==len(data_list))
    return data_list

def query_data(country, indicator, start_date, end_date):
    # example param: '/countries/all/indicators/SP.POP.TOTL?date=2000:2001'
    date = "%s:%s" % (start_date, end_date)
    args = urllib.urlencode({'format':'json',
                              'date':date})
    param = "/countries/%s/indicators/%s?%s" % (country, indicator, args)
    data_list = abstract_query(param)
    indicator = parse_single_country(data_list)
    return indicator

def query_multiple_data(countries, indicator, start_date, end_date):
    pass

def all_indicators():
    param = urllib.urlencode({'format':'json'})
    url = 'http://api.worldbank.org/indicators'
    response = make_request(url + '?' + param)
    #pprint(response)
    return response