'''
Created on 16. 3. 2012.

@author: kermit
'''
from foc.forecaster.ai.output.tsv import TSV
from foc.forecaster.ai.output.sgd import SGDFormat

class Writer(object):
    '''
    writes samples to a file following some :py:class:Format
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def write(self, samples_set, output_formats, output_location, separate_train_test = True):
        for output_format in output_formats:
            formatter = None
            if output_format == "TSV":
                formatter = TSV()
            elif output_format == "SGD":
                formatter = SGDFormat()
            formatter.write_whole_set(samples_set, output_location, separate_train_test)