'''
Created on 21. 5. 2012.

@author: kermit
'''

class IVisualisation(object):
    '''
    Visualiser interface.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def draw(self):
        """
        Draw a figure and return it as a matplotlib object. Must override.
        """
        raise NotImplementedError
