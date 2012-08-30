'''
Created on 24. 8. 2012.

@author: kermit
'''
from pymongo import Connection


class Cacher(object):
    '''
    Cacher
    '''


    def __init__(self, host, port):
        '''
        Constructor
        '''
        self.connection = Connection(host, port)
        self.db = self.connection.cache_db
        self.countries = self.db.countries
        
    def cache(self, countries):
        reprs = [country.json_repr() for country in countries]
        #TODO: update - selector, new document
        self.db.countries.insert(reprs)
            
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
        indicator = self.db.countries.find_one()['indicators'][0]
        dates = indicator["dates"]
        begin_date = dates[0]
        end_date = dates[-1]
        cantains_years = (arg["start_date"]>=begin_date 
                          and arg["end_date"]<=end_date)
            
        if contains_countries and contains_indicators and cantains_years:
            hit = True #TODO: check for indicators & dates
        if hit:
            countries = self.db.countries.find()#TODO: actually get and deserialzie
            return countries
        else:
            return None
    