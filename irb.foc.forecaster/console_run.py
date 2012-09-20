'''
Created on 16. 12. 2011.

@author: kermit
'''
from time import time
from pylab import show

from foc.forecaster.common import conf
from foc.forecaster.ai.samples_set import SamplesSet
from foc.forecaster.ai.output.writer import Writer
from foc.visualiser.data_presenter import vis_conf
from foc.visualiser.data_presenter.matplotlib.visualiser import Visualiser

import sys

# uuu
def run():
    t1 = time()
    print("Configuration loaded from:")
    visualising = (sys.argv[1]=="visualise") 
    if visualising: # we'll only draw stuff
        print(vis_conf.__file__)
        visualiser = Visualiser()
        visualiser.draw()
    else: # we're gonna build a data set
        # conf path
        print(conf.__file__)
        # size estimation
        size_float = 4.
        B = (conf.end_date-conf.start_date+1)*len(conf.countries)*len(conf.indicators)*size_float
        KB = B/1000.
        MB = KB/1000.
        print("Attempting to fetch roughly %.2f KB (%.2f MB) from the World Bank." % (KB, MB))
        
        
        # start work
        
        samples_set = SamplesSet(conf.look_back_years,
                                 conf.cache_enabled,
                                 conf.cache_host,
                                 conf.cache_port)
        samples_set.build_from_crises_file(conf.countries,
                                           conf.indicators,
                                           conf.testing_percentage)
        writer = Writer()
        writer.write(samples_set, conf.output_format, conf.output_location)
    t2 = time()
    print("Done!")
    print("Duration:")
    duration = t2-t1
    print("%.2f s (%.2f min)" % (duration, (duration)/60.))
    if visualising: visualiser.show()
if __name__ == '__main__':
    run()