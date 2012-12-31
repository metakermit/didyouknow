'''
Created on 22. 8. 2012.

@author: kermit
'''

import copy
import time

import wb.api
from cacher import Cacher


class Extractor(object):
    
    def __init__(self):
        self._cache_enabled = False
        self._cache_connection_port = None
        self._cache_connection_host = None
        self._cacher = None
        self._arg = {"country_codes" : ["hrv", "usa"],
               "indicator_codes" : ["SP.POP.TOTL"],
               "start_date" : 1980,
               "end_date" : 2010,
               "pause" : 0}

    def arg(self):
        return copy.deepcopy(self._arg)
    
    def normalize(self, arg):
        if arg==None:
            arg = self.arg()
        if "interval" in arg:
            arg["start_date"], arg["end_date"] = arg["interval"]
        capitalize_list = lambda elems : [el.upper() for el in elems]
        arg["country_codes"] = capitalize_list(arg["country_codes"])
        return arg
    
    def grab(self, arg=None):
        rca_indicators = []
        wb_indicators = []
        
        try:
            import local_storage.rca.api
            # Check if indicator is in RCA dataset, if not then it must be in WB.
            # TODO: Make indicator type checking universal.
            available_rca_indicators = set(local_storage.rca.api.all_indicators()) 
            for indicator_code in arg["indicator_codes"]:
                if indicator_code in available_rca_indicators:
                    rca_indicators.append(indicator_code)
                else:
                    wb_indicators.append(indicator_code)
            
            # Grab RCA data.        
            rca_arg = copy.deepcopy(arg)
            rca_arg["indicator_codes"] = rca_indicators
            rca_countries = self._grab_from_api(rca_arg, local_storage.rca.api)
        except ImportError:
            print("Can't import local_storage.rca.api! Will assume there aren't any indicators from there")
            rca_countries = []
            wb_indicators = arg["indicator_codes"]
        
        # Grab WB data.
        wb_arg = copy.deepcopy(arg)
        wb_arg["indicator_codes"] = wb_indicators
        wb_countries = self._grab_from_api(wb_arg, wb.api)
        
        #TODO: Separate function for merging two or more list of countries.
        # Not assuming that wb and rca countries are in corresponding order in lists.
        all_codes = set()
        wb_dict = {}
        for wb_country in wb_countries:
            all_codes.add(wb_country.code)
            wb_dict[wb_country.code] = wb_country
        rca_dict = {}
        for rca_country in rca_countries:
            all_codes.add(rca_country.code)
            rca_dict[rca_country.code] = rca_country
        combined_countries = []
        for code in all_codes:
            current_countries = []
            try: current_countries.append(wb_dict[code])
            except KeyError: pass
            try: current_countries.append(rca_dict[code])
            except KeyError: pass
            if len(current_countries)!=0:
                if len(current_countries)>1:
                    current_countries[0].merge_with_country(current_countries[1])
                combined_countries.append(current_countries[0])
        return combined_countries
                
#        #TODO: Merge RCA and WB data.
#        # Assumptions is that rca_countries and wb_countries have elements in same order (maybe write unit test for that).
#        for wb_country,rca_country in zip(wb_countries,rca_countries):
#            wb_country.merge_with_country(rca_country)
#        
#        return wb_countries
    
    def _grab_from_api(self, arg=None, api=wb.api):
        #TODO: think about using kwargs
        """
        possible args are:
        
        1) the default by leaving None, defined in arg()
        2) setting your own such as:
                {"country_codes" : ["hrv", "usa", "chn"],
                   "indicator_codes" : ["SP.POP.TOTL"],
                   "start_date":1980,
                   "end_date":2010}
        3) using interval to set the dates more quickly (overrides start/end_date)
                {"country_codes" : ["hrv", "usa", "chn"],
                   "indicator_codes" : ["SP.POP.TOTL"],
                   "interval":(1980,2010)}
        """
        arg = self.normalize(arg)
        if self._cache_enabled:
            countries = self._cacher.retreive(arg)
            if countries: self.cache_hit = True
            else: self.cache_hit = False
        if not self._cache_enabled or not self.cache_hit:
            countries = api.query_multiple_data(
                                                   arg["country_codes"], arg["indicator_codes"],
                                                   arg["start_date"], arg["end_date"])
            if arg["pause"]:
                time.sleep(arg["pause"])
            if self._cache_enabled and not self.cache_hit:
                self._cache(countries)
        return countries
    
    def grab_metadata(self, what="countries", api = wb.api):
        """
        @param what: string of what to get
         - 'countries' - list of countries
         - 'indicators' - list of indicators
        """
        if what=="countries":
            return api.all_countries()
        elif what=="indicators":
            return api.all_indicators()
    
    def enable_cache(self, host="localhost", port=27017, test=False):
        """
        @param host: the hostname of the server where mongodb is running
        @param port: port mongodb is listening on
        @param test: True if you want to work on a db separate than the main cache
        """
        self._cache_connection_host = host
        self._cache_connection_port = port
        self._cache_enabled = True
        self._cacher = Cacher(self._cache_connection_host, self._cache_connection_port, test)
        
    def disable_cache(self):
        self._cache_enabled = False
        
    def clear_cache(self):
        """
        clear everything from the cache
        """
        self._cacher.clear()
    
    def _cache(self,countries):
        if self._cache_enabled:
            self._cacher.cache(countries)
        else: return
    
    def is_cached(self, arg):
        arg = self.normalize(arg)
        countries = self._cacher.retreive(arg)
        if countries: return True
        else: return False
    def was_cached(self):
        """
        tells if the data was found in the cache on the last grab
        """
        return self.cache_hit
