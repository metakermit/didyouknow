'''
Created on 20. 12. 2011.

@author: kermit
'''

CRISIS_CLASS = "crisis"
NORMAL_CLASS = "normal"


class Sample(object):
    '''
    A single pattern recognition sample
    '''


    def __init__(self, features=None, classification=None, description=None):
        '''
        Constructor
        '''
        self.features = features
        self.classification = classification
        self.description = description