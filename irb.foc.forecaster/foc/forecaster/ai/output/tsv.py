'''
Created on 16. 3. 2012.

@author: kermit
'''
from foc.forecaster.ai.output.format import Format
import numbers
from foc.forecaster.ai.preprocessor import is_na
from foc.forecaster.common.exceptions import UnexpectedDataError

class TSV(Format):
    '''
    Tab-separated values output for the Orange ML system.
    '''

    def write(self, metadata, samples, filename):
        '''
        samples - list of samples
        filename - name of output file
        '''
        
        separator = "\t"
        with open(filename, "w") as out:
            # metadata - labels
            out.write("EVENTS%s" % (separator))
            for label in metadata.labels:
                out.write("%s%s" % (label, separator))
            out.write("class\n")
            # actual data
            i = 2
            for sample in samples:
                # description in the 1st column
                out.write("%s%s" % (sample.description, separator))
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
                out.write("%s\n"
                          % (sample.classification))
                
