'''
Created on 20. 12. 2011.

@author: kermit
'''
import numpy as np
import math

from forecaster.common.exceptions import NonExistentDataError

# the NA (not available) value
#TODO: replace with np.NA when numpy >1.7 becomes available
na = np.NaN

def is_na(value):
    return math.isnan(value)

class Preprocessor(object):
    '''
    applies preprocessing operations on a sequence of data
    '''


    def __init__(self, x=None, y=None):
        '''
        Constructor
        '''
        if x!=None and y!=None:
            self.x = np.array(x)
            self.y = np.array(y)
            
    def na(self):
        return na
    
    def maximum(self):
        #maximum = np.max(self.y)
        #index = np.argmax(self.y)
        # or the hard way...
        maximum = -np.inf
        for i in range(len(self.y)):
            if not is_na(self.y[i]) and self.y[i]>maximum:
                maximum = self.y[i]
                index = i
        if maximum == -np.inf: # all values are NA
            maximum = self.na()
            index = self.na()
        return maximum, index
    
    def minimum(self):
        #minimum = np.min(self.y)
        #index = np.argmin(self.y)
        # or the hard way...
        minimum = np.inf
        for i in range(len(self.y)):
            if not is_na(self.y[i]) and self.y[i]<minimum:
                minimum = self.y[i]
                index = i
        if minimum == np.inf: # all values are NA
            minimum = self.na()
            index = self.na()
        return minimum, index
    
    def average(self):
        #return np.mean(self.y)
        # or the hard way...
        #TODO: something is fishy in here, write a test
        total_sum = 0.0
        count = 0
        for el in self.y:
            if not is_na(el):
                total_sum = total_sum + el
                count = count + 1
        if count == 0: # all values are NA
            return self.na()
        else:
            return total_sum/count
    
    def slope(self):
        n = len(self.x)
        # sum of products = x1y1 + x2y2 + . . . + xnyn 
        sum_xy = np.sum(self.x*self.y)
        # sum of x-values = x1 + x2 + . . . + xn 
        sum_x = np.sum(self.x)
        # sum of y-values = y1 + y2 + . . . + yn
        sum_y = np.sum(self.y)
        # sum of squares of x-values = x1^2 + x2^2+ . . . + xn^2
        sum_xx = np.sum(np.power(self.x,2))
        slope = (n*sum_xy-sum_x*sum_y)/(n*sum_xx-np.power(sum_x,2)) 
        return slope
    
    def preprocess_indicator(self, indicator, interesting_years):
        # return [value_1, value_2..., value_n, max, index_max, min,
        #        index_min, average, slope]
        
        # self.x and self.y are numpy arrays for fast calculations
        self.x = np.array(interesting_years)
        self.features = []
        for year in interesting_years:
            try:
                value = indicator.get_value_at(year)
            except NonExistentDataError:
                #raise  # leaving this would propagate the error further and exclude the sample
                value = self.na()
            # first we add the values themselves
            self.features.append(value)
        self.y = np.array(self.features)
        maximum, loc_max = self.maximum()
        minimum, loc_min = self.minimum()
        average = self.average()
        slope = self.slope()
        # append after all the calculations are done!
        # (because otherwise, they would've been taken into account)
        self.features.extend([maximum, loc_max,
                              minimum, loc_min,
                              average, slope])
        return self.features
