'''
Created on 14. 12. 2011.

@author: kermit
'''
from pylab import *

from forecaster.common.exceptions import NonExistentDataError

class Indicator(object):
    '''
    __dates and __values of an indicator for a country
    '''
    #__dates=[]
    #__values=[]

    def __init__(self, dates=None, values=None):
        if dates==None or values==None:
            self.__dates = []
            self.__values = []
        else:
            self.__dates=dates
            self.__values = values
        self.code = ""
        
    def apply_derivative(self):
        new_values = []
        for i in range(1,len(self.dates)):
            value1 = self.values[i-1]
            value2 = self.values[i]
            new_values.append(value2-value1)
        try:
            self.get_dates().pop(0)
        except:
            pass
        self.set_values(new_values)
        
    def get_value_at(self, date):
        try:
            i = self.get_dates().index(date)
        except ValueError:
            raise NonExistentDataError, "the value at the specified year doesn't exist"
        return self.get_values()[i]
    
    def set_value_at(self, date, value):
        self.dates.append(date)
        self.values.append(value)
    
    def merge_with_indicator(self, indicator):
        for date in indicator.get_dates():
            self.set_value_at(date, indicator.get_value_at(date))

    def get_dates(self):
        return self.__dates


    def get_values(self):
        return self.__values


    def set_dates(self, value):
        self.__dates = value


    def set_values(self, value):
        self.__values = value


    def del_dates(self):
        del self.__dates


    def del_values(self):
        del self.__values

    dates = property(get_dates,set_dates, del_dates,
                     "__dates when __values are measured")
    values = property(get_values, set_values, del_values,
                      "indicator __values")

    
    