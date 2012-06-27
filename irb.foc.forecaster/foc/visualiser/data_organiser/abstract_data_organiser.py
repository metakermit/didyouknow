'''
Created on 26. 6. 2012.

@author: kermit
'''

from foc.forecaster.sources.extractor import Extractor

class AbstractDataOrganiser(object):
    '''
    Fetches data using the Extractor and organises it
    in json files for an appropriate visualisation presenter.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._extractor = Extractor()
    
    def _write_data(self):
        """
        @param vis_data: a file where data
        should be stored   
        """
        filename = "data.json"
        with open(filename) as out_file:
            out_file
    
    def _organise_data(self, conf):
        """
        should use the extractor to fetch what is needed
        and format it in a dictionary (store in self.vis_data).
        @attention: must override
        """
        pass
    
    def get_representation(self, conf):
        return self._organise_data(conf)
        