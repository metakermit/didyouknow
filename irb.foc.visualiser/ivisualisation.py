'''
Created on 21. 5. 2012.

@author: kermit
'''
from pylab import *

from forecaster.sources.extractor import Extractor
from forecaster.common.exceptions import MustOverrideError

class IVisualisation(object):
    '''
    Visualiser interface.
    '''
    
    #extractor = None
    #figure = None
    
    def __init__(self):
        '''
        Constructor
        '''
        self.extractor = Extractor()
        self.figure = figure()
        hold(True)
    
    def create(self):
        """
        Create a figure and return it as a matplotlib object. Must override.
        """
        raise MustOverrideError
