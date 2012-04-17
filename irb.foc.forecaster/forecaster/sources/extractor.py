'''
Created on 13. 12. 2011.

@author: kermit
'''
from pprint import pprint
from pylab import *
import time

from forecaster.model.country import Country
from forecaster.model.indicator import Indicator
import wb


class Extractor(object):
    """
    This module fetches the data from some API. 
    This class is here as an independence layer between the forecaster and the World Bank wrapper.
    (in case we decide to use several APIs in the future)
    """
    def __init__(self):
        pass
    
    def process(self, process_indicators):
        for ind_code in self.indicators:
            if ind_code in process_indicators:
                for country in self.countries:
                    country.get_indicator(ind_code).apply_derivative()
    
    def draw(self):
        hold(True)
        #figure()
        grid()
        
        xlabel("year")
        ylabel("value")
        for ind_code in self.indicators:
            for country in self.countries:
                indicator = country.get_indicator(ind_code)
                plot(indicator.dates, indicator.values,
                     label = country.code + " - " + indicator.code)
        legend()
        show()
    
    def fetch_data_per_conf(self, conf):
        # automatic function that
        # fetches all the data specified in the conf file
        return self.fetch_data(conf.countries, conf.indicators,
                               conf.start_date, conf.end_date, conf.wb_pause)

    def fetch_data(self, country_codes, indicator_codes, start_date, end_date, pause=0):
        """
        Fetch indicator values stored in country objects,
        doesn't care of the crises conditions etc.
        gets all the years!!! (which can be a lot of data for many countries)
        
        @param country_codes: a list of country codes to fetch
        @param indicator_codes: a list of indicator codes to fetch
        @param start_date: a year from which indicators that we want to fetch should start
        @param end_date: a year from which indicators that we want to fetch should end
        @param pause: a pause in number of seconds between two queries (to ease the load on the World Bank API); unused in this method
        
        @return: a list of country objects
        """
        self.countries = wb.query_multiple_data(country_codes, indicator_codes, start_date, end_date)
        self.indicators = indicator_codes
        return self.countries
    
    def fetch_data_separate_queries(self, country_codes, indicator_codes, start_date, end_date, pause=0):
        """
        Fetch indicator values stored in country objects,
        doesn't care of the crises conditions etc.
        gets all the years!!! (which can be a lot of data for many countries)
        
        @param country_codes: a list of country codes to fetch
        @param indicator_codes: a list of indicator codes to fetch
        @param start_date: a year from which indicators that we want to fetch should start
        @param end_date: a year from which indicators that we want to fetch should end
        @param pause: a pause in number of seconds between two queries (to ease the load on the World Bank API)
        
        @return: a list of country objects
        @deprecated: this method makes a separate query for each country, fetch_data should be used
        """
        # 
        
        country_list = []
        for cnt_code in country_codes:
            country = Country(cnt_code)
            for ind_code in indicator_codes:
                indicator = self.fetch_indicator(country.code,
                                                 ind_code,
                                                 start_date,
                                                 end_date)
                time.sleep(pause)
                indicator.code = ind_code
                country.set_indicator(indicator)
            country_list.append(country)
        self.indicators = indicator_codes
        self.countries = country_list
        return self.countries
    
    def fetch_data_sparse(self, country_codes, indicator_codes, event_boundaries, pause=0):
        """
        We fetch data only for the years that we need, specified in event_boundaries
        @deprecated: this method makes a lot of queries - it is generally better to make fewer queries, even if it means fetching some data we don't need.
        """
        country_list = []
        for cnt_code in country_codes:
            country = Country(cnt_code)
            for ind_code in indicator_codes:
                indicator = Indicator()
                for event in event_boundaries[cnt_code]:
                    begin, end = event
                    indicator_part = self.fetch_indicator(country.code,
                                                     ind_code,
                                                     begin,
                                                     end)
                    time.sleep(pause)
                    indicator.merge_with_indicator(indicator_part)
                indicator.code = ind_code
                country.set_indicator(indicator)
            country_list.append(country)
        self.indicators = indicator_codes
        self.countries = country_list
        return self.countries
    
    def fetch_indicator(self, country, indicator, start_date, end_date):
        """
        gets all the indicator data within the period for the _country_
        """ 
        return wb.query_data(country, indicator, start_date, end_date)
    
    def run(self, conf):
        country_list = self.fetch_data_per_conf(conf)
        self.process(conf.process_indicators)
        self.draw()