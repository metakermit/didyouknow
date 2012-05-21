'''
Created on 16. 12. 2011.

@author: kermit
'''
from pylab import *
import os

from forecaster.sources.extractor import Extractor
import multigroup_visualiser as mv
import conf


def draw_time_series():
    """
    draw single time series line plots for the data defined in the conf file
    """
    extractor = Extractor()
    extractor.fetch_data_per_conf(conf)
    extractor.process(conf.process_indicators)
    extractor.draw()
    
def draw_multigroup():
    vis = mv.MultigroupVisualisation()
    print conf.groups
    
    fig = figure()
    hold(True)
    suptitle(conf.graph_title, fontsize=16)
    #grid()
    #colors = ["r","b","g","y"]
    i = 0
    for group in conf.groups:
        vis.add_to_graph(group, conf.colors[i], conf.legend[i], conf.indicator_titles, conf.label_dist_factor)
        i+=1
    legend(scatterpoints=1, loc=conf.legend_loc, fancybox=True)
    return fig

def draw_complete_multigroup():
    """
    draw a time series marked with crisis and model data
    for the data defined in the conf file
    """
    pass



def run():
    """
    Entry point to the visualiser. Call visualisation method to get the figure and draw it (in a file or live). 
    """
    fig = None
    visualisation = conf.visualisation()
    fig = visualisation.draw()
    if not fig==None:
        if conf.write_to_file:
            fig.savefig(conf.filename, format=os.path.splitext(conf.filename)[1][1:])
        else:
            show()

if __name__ == '__main__':
    run()