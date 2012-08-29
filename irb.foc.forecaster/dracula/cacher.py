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
        self.db.countries.insert(reprs)
            
    def retreive(self, arg):
        hit = False
        wanted_countries = set(arg["country_codes"])
        for country in self.db.countries.find():
            code = country["code"]
            try: wanted_countries.remove(code)
            except KeyError: pass
        if len(wanted_countries) == 0: # empty
            # all countries covered
            hit = True #TODO: check for indicators & dates
        
        if hit:
            countries = self.db.countries.find()#TODO: actually get and deserialzie
            return countries
        else:
            return None
    