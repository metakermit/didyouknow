'''
Created on 10. 1. 2012.

@author: kermit
'''

from forecaster.ai.sample import CRISIS_CLASS, NORMAL_CLASS

class Format(object):
    '''
    abstract format for writing train and test samples to files
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def translate_to_numeric(self, classification):
        if classification == CRISIS_CLASS:
            return 1
        if classification == NORMAL_CLASS:
            return 2
    
    def write(self, metadata, samples, filename):
        pass
    
    def write_whole_set(self, samples_set):
        self.write(samples_set.metadata, samples_set.test_samples, "dataset-test.txt")
        self.write(samples_set.metadata, samples_set.train_samples, "dataset-train.txt")

    