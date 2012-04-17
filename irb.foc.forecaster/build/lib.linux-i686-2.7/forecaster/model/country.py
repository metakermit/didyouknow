'''
Created on 14. 12. 2011.

@author: kermit
'''

class Country(object):
    '''
    __indicators concerning a single country
    '''
    #__code = ""
    #__indicators = {}

    def __init__(self, code):
        '''
        __code - code of a country
        '''
        self.__code = code
        self.__indicators = {}

    def get_code(self):
        return self.__code

        
    def indicator_codes(self):
        return self.__indicators.keys()

    def get_indicator(self, code):
        return self.__indicators[code]


    def set_indicator(self, code, indicator):
        self.__indicators[code] = indicator


    def del_indicators(self):
        del self.__indicators

    #__indicators = property(get_indicator, set_indicator, del_indicators,
    #                      "a dictionary with individual __indicators")
    code = property(get_code, None, None, None)
        
    