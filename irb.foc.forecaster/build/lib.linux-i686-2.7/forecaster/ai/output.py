'''
Created on 10. 1. 2012.

@author: kermit
'''
import numbers

from forecaster.ai.sample import CRISIS_CLASS, NORMAL_CLASS
from forecaster.ai.preprocessor import is_na
from forecaster.common.exceptions import UnexpectedDataError

class Output(object):
    '''
    wrapper for writing train and test samples in a formatted textual file
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
        '''
        samples - list of samples
        filename - name of output file
        '''
        desc_filename = "description-"+filename
        
        separator = " "
        with open(filename, "w") as out, open(desc_filename, "w") as desc:
            # header
            out.write("Number of examples %d\n" % (len(samples)))
            try:
                samples_number = len(samples[0].features)
            except IndexError:
                samples_number = 0
            out.write("Number of inputs %d\n" % (samples_number))
            # metadata - types
            out.write("n%s" % (separator))
            for data_type in metadata.types:
                out.write("%s%s" % (data_type, separator))
            out.write("o\n")
            # metadata - labels
            out.write("no%s" % (separator))
            for label in metadata.labels:
                out.write("%s%s" % (label, separator))
            out.write("class\n")
            # actual data
            i = 1
            for sample in samples:
                # ordinal number
                out.write("%d%s" % (i, separator))
                # description in a separate file
                desc.write("%d%s%s\n" % (i, separator, sample.description))
                i = i + 1
                # value
                for value in sample.features:
                    if is_na(value):
                        out.write("?%s" % (separator))
                    elif isinstance(value, numbers.Integral):
                        int_value = int(value)
                        out.write("%d%s" % (int_value, separator))
                    elif isinstance(value, numbers.Real):
                        out.write("%2.2f%s" % (value, separator))
                    else:
                        raise UnexpectedDataError
                # class
                out.write("%d\n"
                          % (self.translate_to_numeric(sample.classification)))
    
    def write_whole_set(self, samples_set):
        self.write(samples_set.metadata, samples_set.test_samples, "dataset-test.txt")
        self.write(samples_set.metadata, samples_set.train_samples, "dataset-train.txt")
