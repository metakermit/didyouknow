'''
Created on 15. 12. 2011.

@author: kermit
'''
import urllib
import urllib2
import time
# I use json here, but the API also supports xml and jsonp
import json
#from pprint import pprint


import parser

def _make_request(query):
    """
    Exectue the actual query on the World Bank API using urllib2.
    @param query: full url of the query,
    e.g. 'http://api.worldbank.org/countries/all/indicators/SP.POP.TOTL?date=2000:2001'
    @return: response as a list of string objects (directly parsed from json)
    """
    attempts = 3
    sucess = False
    while attempts>0 and sucess!=True:
        try:
            # do the actual query
            http_response = urllib2.urlopen(query)
            # and if an exception wasn't thrown we did it!
            sucess = True
        except urllib2.HTTPError, e:
            print("World Bank server error, giving it another try.")
            # that was one unsuccessful attempt
            attempts-=1
            if attempts == 0:
                # OK, we won't try any more
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
                #print('Reason: ', e.reason)
                raise
            # let the World Bank cool down a bit :)
            time.sleep(10)
    data = json.load(http_response)
    return data

def _abstract_query(parameters):
    """
    An abstract query that "doesn't know" what it's asking from the WB.
    Hides the complexity of joining multiple pages.
    @param parameters: a string with parameters to the API
    e.g. "/countries/hrv/indicators/SP.POP.TOTL"
    @return: a list of response string objects
    """
    read_pages=0
    # for now we assume there's gonna be only 1 page
    # we'll find out the exact no. in the 1st response
    total_pages=1
    # build url request
    root = 'http://api.worldbank.org'
    url = root + parameters
    #example url:
    #'http://api.worldbank.org/countries/hrv/indicators/SP.POP.TOTL'

    data_list = [] # we store the responses here
    while(read_pages<total_pages):
        try:
            # query results from the current page
            query = url + '&page=' + str(read_pages+1)
            # the actual query is executed by the _make_request function
            response = _make_request(query)
        except urllib2.HTTPError:
            #error_msg = "Was fetching indicator %s for country %s between %s and %s."
            #print error_msg % (indicator, country, start_date, end_date)
            print "The query was:\n" + query + "\n" 
            raise
        
        # btw response[0] is the information on the pages etc,
        # actual data is in a list at index 1
        # add the items from this page to the main list 
        data_list.extend(response[1])
        total_pages = response[0]['pages']
        if read_pages==0 and total_pages>10:
            print("Have to query %d pages, expect some latency" % (total_pages))
        read_pages = read_pages + 1
    # response[1] contains a list of dictionaries - one dic per year
    #pprint(data_list)
    # check to see if all of the http_response is loaded
    assert(response[0]['total']==len(data_list))
    return data_list

def query_data(country, indicator, start_date, end_date):
    #example param: '/countries/all/indicators/SP.POP.TOTL?date=2000:2001'
    date = "%s:%s" % (start_date, end_date)
    args = urllib.urlencode({'format':'json',
                              'date':date})
    param = "/countries/%s/indicators/%s?%s" % (country, indicator, args)
    data_list = _abstract_query(param)
    return parser.parse_single_country(data_list)

def _query_multiple_countries(countries=['all'], indicator='', start_date=2010, end_date=2011):
    """
    Single query (not counting pages) to get a single country's data.
    @param countires: list of country codes to fetch e.g. ['usa','bra']
    """
    date = "%s:%s" % (start_date, end_date)
    # how many data per page will be shown
    per_page=12000
    if indicator=='':
        args = urllib.urlencode({'format':'json',
                              'per_page':per_page})
        param = "/countries/%s?%s" % (";".join(countries), args)
        data_list = _abstract_query(param)
        return parser.parse_multiple_countries_alone(data_list)
    else:
        args = urllib.urlencode({'format':'json',
                              'date':date,
                              'per_page':per_page})
        param = "/countries/%s/indicators/%s?%s" % (";".join(countries), indicator, args)
        data_list = _abstract_query(param)
        return parser.parse_multiple_countries(data_list, start_date, end_date)
    #data_list = _abstract_query(param)
    #return parse_single_country(data_list)

def query_multiple_data(country_codes=['all'], indicator_codes=[], start_date=2010, end_date=2011):
    """
    Perform several queries if necessary to get a multiple indicator tables.
    Parse them and return them as country objects
    @param country_codes: list of country codes to fetch e.g. ['usa','bra']
    @param indicator_codes: list of indicator codes to fetch
    @param start_date: a year from which indicator_codes that we want to fetch should start
    @param end_date: a year from which indicator_codes that we want to fetch should end
    @param pause: a pause in number of seconds between two queries (to ease the load on the World Bank API); unused in this method
        
    @return: a list of country objects
    """
    num_queries = len(indicator_codes)
    verbose=False 
    if num_queries>10:
        print("Will have to perform %d indicator table queries (not counting pages)" % (num_queries))
        verbose=True
    done_queries = 0
    countries = _query_multiple_countries(country_codes)
    if not num_queries==0: # we will get indicators if they are needed at all
        country_indicators=[] # this is a list of lists of country_codes (to be merged later)
        for indicator in indicator_codes:
            countries_with_single_indicator = _query_multiple_countries(country_codes, indicator, start_date, end_date)
            done_queries+=1
            if verbose:
                print("%d/%d" % (done_queries,num_queries))
            country_indicators.append(countries_with_single_indicator)
        parser.add_indicators_to_countries(countries, country_indicators)
    return countries

def _simple_query(params):
    """
    Adds the common stuff and passes on the query.
    """
    args = urllib.urlencode({'format':'json'})
    complete_param = '%s?%s' % (params, args)
    data_list = _abstract_query(complete_param)
    #url = 'http://api.worldbank.org/indicators'
    #response = _make_request(url + '?' + complete_param)
    #pprint(response)
    return data_list

def all_indicators():
    return _simple_query("/indicators")

def all_countries():
    return _simple_query("/countries")
