'''
Created on 16. 12. 2011.

@author: kermit
'''
from time import time

from foc.forecaster.sources.extractor import Extractor
from foc.forecaster.common import conf
from foc.forecaster.ai.samples_set import SamplesSet
from foc.forecaster.ai.output.writer import Writer

# uuu
def draw():
    #extractor = Extractor()
    #countries = extractor.fetch_data_per_conf(conf)
    
    # size estimation
    size_float = 4.
    B = (conf.end_date-conf.start_date+1)*len(conf.countries)*len(conf.indicators)*size_float
    KB = B/1000.
    MB = KB/1000.
    print("Attempting to fetch roughly %.2f KB (%.2f MB) from the World Bank." % (KB, MB))
    
    t1 = time()
    # start work
    samples_set = SamplesSet(conf.look_back_years)
    samples_set.build_from_crises_file(conf.countries,
                                       conf.indicators,
                                       conf.testing_percentage,
                                       sparse=conf.sparse)
    writer = Writer()
    writer.write(samples_set, conf.output_format)
    t2 = time()
    print("Done!")
    print("Duration:")
    duration = t2-t1
    print("%.2f s (%.2f min)" % (duration, (duration)/60.))

if __name__ == '__main__':
    draw()