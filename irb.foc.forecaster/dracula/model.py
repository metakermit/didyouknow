'''
Created on 22. 8. 2012.

@author: kermit
'''
import copy

class Country(object):
    '''
    A representation of a single country,
    aggregates indicators.
    '''

    def __init__(self, code):
        '''
        @code - code of a country
        '''
        self.code = code
        self.code_iso2 = ""
        # a dictionary with individual indicators
        self.indicators = {}
        self.indicator_codes = []
    
    def __str__(self):
        return self.code
    
    def __repr__(self):
        return self.code

    def get_indicator(self, code):
        return self.indicators[code]

    def set_indicator(self, indicator):
        self.indicators[indicator.code] = indicator
        self.indicator_codes.append(indicator.code)
        
    def json_repr(self):
        """serialize to json"""
        indicators_repr = [ind.json_repr() for ind in self.indicators.values()]
        me = {'code': self.code,
                'code_iso2': self.code_iso2,
                'indicators': indicators_repr, 
                'indicator_codes': self.indicator_codes
        } 
        return me
    
    def merge_with_country(self, new_country):
        """ Merge indicators from other country object."""
        #TODO: Check the codes to see if they are really the same country.
        for new_indicator in new_country.indicator_codes:
            if new_indicator in self.indicator_codes:
                pass
            else:
                self.set_indicator(new_country.indicators[new_indicator])
    
    @staticmethod
    def from_json(country_repr):
        """deserialize from json"""
        me = Country(country_repr["code"])
        for indicator_repr in country_repr["indicators"]:
            indicator = Indicator.from_json(indicator_repr)
            me.set_indicator(indicator)
        me.code_iso2=country_repr["code_iso2"]
        return me
        
from dracula.exceptions import NonExistentDataError
from foc.forecaster.ai.preprocessor import Preprocessor

class Indicator(object):
    '''
    dates and values of an indicator for a country
    '''

    def __init__(self, code=None, dates=None, values=None, nominal_start=None, nominal_end=None): 
        if dates==None or values==None:
            self.dates = []
            self.values = []
        else:
            self.dates=dates
            self.values = values
        self.code = code
        # nominal years for which the data was queried
        # not all these years are necessarily represented in the data
        # (for caching purposes) 
        self.nominal_start = nominal_start
        self.nominal_end = nominal_end
        
    def simple_dict_repr(self):#TODO:eliminate and replace with json_repr
        return {'code': self.code, 'dates': self.dates, 'values': self.values,
                'nominal_start': self.nominal_start, 'nominal_end': self.nominal_end}
        
    def apply_derivative(self, *args):
        """
        @param *args: arguments tuple, unused here 
        """
        new_values = []
        for i in range(1,len(self.dates)):
            value1 = self.values[i-1]
            value2 = self.values[i]
            new_values.append(value2-value1)
        try:
            self.dates.pop(0)
        except:
            pass
        self.values = new_values
        
    def apply_slope(self, *args):
        """
        @param *args:
        look_back_year - integer stating how many
        values back to look in the slope
        """
        #TODO: move this method to preprocessor & get rid of the foc dependency
        look_back_years = args[0]
        new_values = []
        past_values = []
        past_dates = []
        for i in range(len(self.dates)):
            past_dates.append(self.dates[i])
            past_values.append(self.values[i])
            if i>=look_back_years-1:
                new_values.append(Preprocessor(past_dates,past_values).slope())
                past_dates.pop(0)
                past_values.pop(0)
        try:
            [self.dates.pop(0) for i in range(look_back_years-1)]
        except:
                    pass
        self.values = new_values
        
    def get_value_at(self, date):
        try:
            #i = self.dates().index(date)
            i = self.dates.index(date)
        except ValueError:
            raise NonExistentDataError, "the value at the specified year doesn't exist"
        #return self.values()[i]
        return self.values[i]
    
    def set_value_at(self, date, value):
        self.dates.append(date)
        self.values.append(value)
    
    def merge_with_indicator(self, indicator):
        for date in indicator.dates():
            self.set_value_at(date, indicator.get_value_at(date))
    
    def slice(self, start, end):#TODO: unittest or use Pandas and their built-in slicing
        """ @return: a copy of indicator extra data with sliced off """
        new_indicator = copy.deepcopy(self)
        new_indicator.dates = []
        new_indicator.values = []
        index_start, index_end = None, None
        if len(self.dates) == 0:
            return new_indicator # the range contains nothing
        # find first position
        if start<self.dates[0]:
            index_start = 0
        else:
            for i in range(0, len(self.dates)):
                if self.dates[i]>=start:
                    index_start = i
                    break
            return new_indicator
        # find last position
        if end>self.dates[-1]: 
            index_end = -1 
        else:
            for i in range(len(self.dates), 0):
                if self.dates[i]<=end:
                    index_end = i
                    break
        if index_start==None or index_end==None:
            return new_indicator # the intersection is empty
        # take slice
        new_indicator.dates = self.dates[index_start:index_end+1]
        new_indicator.values = self.values[index_start:index_end+1]
        return new_indicator
            
    def json_repr(self):
        me = {'code': self.code, 'dates': self.dates, 'values': self.values,
                'nominal_start': self.nominal_start, 'nominal_end': self.nominal_end}
        return me
    
    @staticmethod
    def from_json(indicator_repr):
        me = Indicator(code=indicator_repr["code"],
                       dates = indicator_repr["dates"],
                       values = indicator_repr["values"],
                       nominal_start = indicator_repr["nominal_start"],
                       nominal_end = indicator_repr["nominal_end"])
        return me

    
    