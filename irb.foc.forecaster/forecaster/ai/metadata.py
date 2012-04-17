'''
Created on 11. 1. 2012.

@author: kermit
'''

nampply = lambda name, labels :  ["%s_%s" % (name, label) for label in labels]

class Metadata(object):
    '''
    samples set metadata
    '''
    types = []
    labels = []
    
    train_rows = []
    test_rows = []
    
    def multiply_for_all_indicators(self, indicators_with_translations):
        old_labels = self.labels
        old_types = self.types
        self.labels = []
        self.types = []
        i = 0
        for indicator in indicators_with_translations:
            i = i+1
            try:
                name =  indicator.split("-")[1]
            except IndexError:
                name = "ind"+str(i)
            self.labels.extend(nampply(name, old_labels))
            self.types.extend(old_types)
        
    def __init__(self, conf, look_back_years):
        '''
        Constructor
        '''
        # look_back_years - the number of years that
        #                         are looked at as crises causes
        delta = range(look_back_years)
        self.labels = ["t_%d" % (look_back_years - el) for el in delta]
        self.labels.extend(["max", "index_max",
                            "min", "index_min",
                            "average", "slope"])
        self.types = ["f"] * look_back_years
        self.types.extend(["f", "f", "f", "f", "f", "f"])
        self.multiply_for_all_indicators(conf.indicators_with_translations)
    
    def get_metadata(self):
        """
        return a list of column names and a list of column types
        """
        return self.labels, self.types
    
    def get_rows(self):
        """
        
        """
