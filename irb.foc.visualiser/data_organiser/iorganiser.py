'''
Created on 1. 6. 2012.

@author: kermit
'''

class IOrganiser(object):
    '''
    Fetches data using the Extractor and organises it
    in CSV files for an appropriate visualisation presenter.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def _write_data(self, vis_data):
        """
        @param vis_data: CSV file where data
        should be stored   
        """
    
    def organise_data(self):
        filename = "data.csv"
        with open(filename) as vis_data:
            self._write_data(vis_data)
