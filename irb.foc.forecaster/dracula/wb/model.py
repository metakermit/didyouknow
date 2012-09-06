'''
Created on 22. 8. 2012.

@author: kermit
'''

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
        indicators_repr = [ind.json_repr() for ind in self.indicators.values()]
        me = {'code': self.code,
                'code_iso2': self.code_iso2,
                'indicators': indicators_repr, 
                'indicator_codes': self.indicator_codes
        } 
        return me
        
from dracula.exceptions import NonExistentDataError
from foc.forecaster.ai.preprocessor import Preprocessor

class Indicator(object):
    '''
    dates and values of an indicator for a country
    '''

    def __init__(self, code=None, dates=None, values=None):
        if dates==None or values==None:
            self.dates = []
            self.values = []
        else:
            self.dates=dates
            self.values = values
        self.code = code
        
    def simple_dict_repr(self):
        return {'code': self.code, 'dates': self.dates, 'values': self.values}
        
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
        self.set_values(new_values)
        
    def apply_slope(self, *args):
        """
        @param *args:
        look_back_year - integer stating how many
        values back to look in the slope
        """
        #TODO: move this method to preprocessor
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
        self.set_values(new_values)
        
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
            
    def json_repr(self):
        me = {'code': self.code, 'dates': self.dates, 'values': self.values}
        return me

    
    