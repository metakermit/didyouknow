'''
Created on 16. 3. 2012.

@author: kermit
'''
from forecaster.ai.output.tsv import TSV
from forecaster.ai.output.sgd import SGDFormat

class Writer(object):
    '''
    writes samples to a file following some :py:class:Format
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def write(self, samples_set, output_format):
        formatter = None
        if output_format == "TSV":
            formatter = TSV()
        elif output_format == "SGD":
            formatter = SGDFormat()
        formatter.write_whole_set(samples_set)