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
            return None
    