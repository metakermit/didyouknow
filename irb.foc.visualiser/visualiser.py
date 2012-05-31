'''
Created on 16. 12. 2011.

@author: kermit
'''

import conf
from ts_visualisation import TimeSeriesVisualisation
from multigroup_visualisation import MultigroupVisualisation
from complete_multigroup_visualisation import CompleteMultigroupVisualisation
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
    vis_str = conf.visualisation
    if vis_str == "TSV":
        visualisation = TimeSeriesVisualisation()
    elif vis_str == "MV":
        visualisation = MultigroupVisualisation()
    elif vis_str == "CMV":
        visualisation = CompleteMultigroupVisualisation()
    visualisation.create_all_figures()
    

if __name__ == '__main__':
    draw()