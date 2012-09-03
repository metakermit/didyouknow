'''
Created on 16. 12. 2011.

@author: kermit
'''

import conf
from ts_visualisation import TimeSeriesVisualisation
from multigroup_visualisation import MultigroupVisualisation
from complete_multigroup_visualisation import CompleteMultigroupVisualisation
from forecaster.common.exceptions import ConfigurationFileError
from data_organiser.iorganiser import IOrganiser
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

def get_workers():
    vis_str = conf.visualisation
    if vis_str == "TSV":
        organiser = IOrganiser()
        visualisation = TimeSeriesVisualisation()
    elif vis_str == "MV":
        visualisation = MultigroupVisualisation()
    elif vis_str == "CMV":
        visualisation = CompleteMultigroupVisualisation()
    else:
        raise ConfigurationFileError
    return organiser, visualisation

def draw():
    """
    Entry point to the visualiser. Call visualisation method to get the figure and create it (in a file or live). 
    """
    organiser, visualisation = get_workers()
    organiser.organise_data()
    visualisation.create_all_figures()

if __name__ == '__main__':
    draw()
    