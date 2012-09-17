'''
Created on 30. 5. 2012.

@author: kermit
'''
from foc.forecaster.ai.input import Input

class CrisisSeer(object):
    '''
    Knows when a crisis occured in a certain country (based
    on the crisis database)
    '''


    def __init__(self, db_location):
        '''
        Constructor
        '''
        self.input = Input()
        self.crises, self.normals = self.input.parse_sample_selection(db_location)
        
    def get_crisis_years(self, country_code):
        """
        return a list of years when this country had crises
        """
        events_list = []
        try:
            events_list = self.crises[country_code]
        except KeyError:
            # this country has no noted crises so we'll suppose
            # it's crisis-free
            pass
        return events_list
        