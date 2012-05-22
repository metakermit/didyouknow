'''
Created on 16. 12. 2011.

@author: kermit
'''
from pylab import *
import os

import conf
#===============================================================================
# 
# 
# def draw_time_series():
#    """
#    create single time series line plots for the data defined in the conf file
#    """
#    extractor = Extractor()
#    extractor.fetch_data_per_conf(conf)
#    extractor.process(conf.process_indicators)
#    extractor.create()
#===============================================================================

def draw():
    """
    Entry point to the visualiser. Call visualisation method to get the figure and create it (in a file or live). 
    """
    fig = None
    visualisation = conf.visualisation()
    fig = visualisation.create()
    if not fig==None:
        if conf.write_to_file:
            fig.savefig(conf.filename, format=os.path.splitext(conf.filename)[1][1:])
        else:
            show()

if __name__ == '__main__':
    draw()