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
    
    def fetch_data(self, country_codes, indicator_codes, start_date, end_date, wb_pause):
        # fetch indicator values
        # (through the date, countries and indicators parameters)
        # doesn't care of the crises conditions etc.
        # gets all the years!!! (which can be a lot of data for many countries)
        country_list = []
        for cnt_code in country_codes:
            country = Country(cnt_code)
            for ind_code in indicator_codes:
                indicator = self.fetch_indicator(country.code,
                                                 ind_code,
                                                 start_date,
                                                 end_date)
                time.sleep(wb_pause)
                indicator.code = ind_code
                country.set_indicator(ind_code, indicator)
            country_list.append(country)
        self.indicators = indicator_codes
        self.countries = country_list
        return self.countries
    
    def fetch_data_sparse(self, country_codes, indicator_codes, event_boundaries, wb_pause):
        """
        We fetch data only for the years that we need, specified in event_boundaries
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
                    time.sleep(wb_pause)
                    indicator.merge_with_indicator(indicator_part)
                indicator.code = ind_code
                country.set_indicator(ind_code, indicator)
            country_list.append(country)
        self.indicators = indicator_codes
        self.countries = country_list
        return self.countries
    
    def fetch_indicator(self, country, indicator, start_date, end_date):
        # gets all the indicator data within the period for the _country_ 
        return wb.query_data(country, indicator, start_date, end_date)
    
    def run(self, conf):
        country_list = self.fetch_data_per_conf(conf)
        self.process(conf.process_indicators)
        self.draw()