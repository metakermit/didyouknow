'''
Created on 24. 8. 2012.

@author: kermit
'''
from pymongo import Connection

from dracula.wb.model import Country

class Cacher(object):
    '''
    Cacher
    '''
    def __init__(self, host="localhost", port=27017, test=False):
        '''
        Constructor
        @param host: the hostname of the server where mongodb is running
        @param port: port mongodb is listening on
        @param test: True if you want to work on a db separate than the main cache
        """
        '''
        self.connection = Connection(host, port)
        if test:
            self.db = self.connection.test_cache_db
        else:
            self.db = self.connection.cache_db
        self.countries = self.db.countries
        
    def cache(self, countries):
        #old & wrong way - inserting
        #reprs = [country.json_repr() for country in countries]
        #self.db.countries.insert(reprs)
        # new way - upserts
        #--------------------------
        # spec - we select all documents
        # document - what we want the new data to be (replaces old!)
        # upsert - insert if there is nothing under those keys
        for country in countries:
            country_repr = country.json_repr()
            self.db.countries.update(spec={"code": country.code},
                                     document=country_repr, upsert=True)
            
    def retreive(self, arg):
        hit = False
        contains_countries, contains_indicators = False, True
        wanted_countries = set(arg["country_codes"])
        for country in self.db.countries.find():
            # check each country's indicators
            wanted_indicators = set(arg["indicator_codes"]) 
            have_indicators = set(country["indicator_codes"])
            if not wanted_indicators.issubset(have_indicators):
                contains_indicators = False
                break
            # check countries
            code = country["code"]
            try: wanted_countries.remove(code)
            except KeyError: pass
        if len(wanted_countries) == 0: # empty
            # all countries covered
            contains_countries = True
        # check years
        try:
            indicator = self.db.countries.find_one()['indicators'][0]
            dates = indicator["dates"]
            begin_date = dates[0]
            end_date = dates[-1]
            cantains_years = (arg["start_date"]>=begin_date 
                              and arg["end_date"]<=end_date)
        except TypeError: # there aren't any indicators
            contains_years = False
            
        if contains_countries and contains_indicators and cantains_years:
            hit = True
        if hit:
            countries_raw = list(self.db.countries.find())#TODO: actually get and deserialzie
            countries = [Country.from_json(country) for country in countries_raw]
            return countries
        else:
            return None
    def clear(self):
        """
        delete everything from the currently selected cache DB
        """
        self.db.countries.remove()