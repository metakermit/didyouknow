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
        self.connection = Connection(host = host, port = port)
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
                                     document=country_repr, upsert=True, safe=True)
            
    def retreive(self, arg):
        """
        Checks the cache for data defined by arg and returns it if it's there
        @param arg: same as for Extractor.grab() 
        @return: data specified by the arg or None if it's a cache miss
        """
        # deserialize what's in the DB
        countries_raw = list(self.db.countries.find())
        cached_countries = [Country.from_json(country) for country in countries_raw]
        # let's pick what we need from it
        target_countries = []
        contains_countries, contains_indicators, contains_years = True, True, True
        wanted_countries = set(arg["country_codes"])
        for country in cached_countries:
            # add the countries we need
            if country.code in wanted_countries:
                target_countries.append(country)
                wanted_countries.remove(country.code)
                # now for that country, let's go see if we have the indicators
                wanted_indicators = set(arg["indicator_codes"])
                for indicator in country.indicators.values():
                    if indicator.code in wanted_indicators:
                        wanted_indicators.remove(indicator.code)
                        # cool, it's here; now let's check for its years
                        begin_date = indicator.nominal_start
                        end_date = indicator.nominal_end
                        interval_satisfied = (arg["start_date"]>=begin_date 
                                              and arg["end_date"]<=end_date)
                        if interval_satisfied: #all past indicators contained years
                            # now we set the data to be
                            # only the years that were asked for 
                            index_begin = indicator.dates.index(arg["start_date"])
                            index_end = indicator.dates.index(arg["end_date"])
                            indicator.dates = indicator.dates[index_begin:index_end+1]
                            indicator.values = indicator.values[index_begin:index_end+1]
                        else:
                            contains_years = False
                    else: # we don't even want that one
                        country.indicators.remove(indicator)
                if len(wanted_indicators)>0: contains_indicators = False
        if len(wanted_countries) > 0: # empty
            # all countries covered
            contains_countries = False
        # all 3 conditions must be true, no data can be missing
        if contains_countries and contains_indicators and contains_years:
            return target_countries
        else: # we have a cache miss
            return None
        
        
    def clear(self):
        """
        delete everything from the currently selected cache DB
        """
        self.db.countries.remove()