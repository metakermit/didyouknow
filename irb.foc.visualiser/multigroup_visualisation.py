'''
Created on 8. 2. 2012.

@author: kermit
'''
from pylab import *

from forecaster.sources.extractor import Extractor
import conf
from forecaster.common.exceptions import NonExistentDataError
from ivisualisation import IVisualisation 

import os

class MultigroupVisualisation(IVisualisation): 
    def __init__(self):
        self.extractor = Extractor()
        
    def fetch_event_data(self, country_code, start, end):
        """
        get data for a single event
        """
        countries = self.extractor.fetch_data([country_code], conf.indicators, start, end, conf.wb_pause)
        self.extractor.process(conf.process_indicators)
        return countries[0]
    
    def add_to_graph(self, group, color, legend_label, indicator_titles, label_dist_factor):
        drawn_legend=False
        for event in group:
            event_data = event.split("-")
            country_code = event_data[0].lower()
            event_year = int(event_data[1])
            start = event_year-conf.years_before
            end = event_year+conf.years_after+1
            country = self.fetch_event_data(country_code, start, end)
            x_ind_code,y_ind_code = country.indicator_codes()[:2]
            x_ind = country.get_indicator(x_ind_code)
            y_ind = country.get_indicator(y_ind_code)
            years = range(start, end)
            i = 0
            all_x = []
            all_y = []
            first = True
            label_text = event
            for t in years:
                try:
                    x = x_ind.get_value_at(t)
                    y = y_ind.get_value_at(t)
                    all_x.append(x)
                    all_y.append(y)
                    xlabel(indicator_titles[x_ind_code])
                    ylabel(indicator_titles[y_ind_code])
                    current_legend_label = None
                    if first:
                        #annotate(label_text, xy=(x,y))
                        first =False
                    if t == event_year:
                        if not drawn_legend:
                            current_legend_label=legend_label
                            drawn_legend = True
                        dist = math.sqrt(math.pow(x-x_ind.get_value_at(t-1),2)+math.pow(y-y_ind.get_value_at(t-1),2))*label_dist_factor
                        annotate(label_text, size="medium" , xy=(x+dist,y+dist))
                        mark = 'd'
                    else:
                        mark = 'o'
                    scatter(x, y, s=1+i, c=color,
                            alpha=0.6, marker=mark,
                            label = current_legend_label)
                    
                    i+=40
                except NonExistentDataError:
                    pass
            if len(all_x)!=len(all_y): # there is no data for one of the indicators
                print "Error: number of data points to be plotted not equal"
                raise NonExistentDataError
            try:
                plot(all_x,all_y, c=color)
            except ValueError:
                print "Something wrong with data to be plotted"
                raise
            
    def draw(self):
        hold(True)
        fig = figure()
        suptitle(conf.graph_title, fontsize=16)
        #grid()
        #colors = ["r","b","g","y"]
        i = 0
        for group in conf.groups:
            self.add_to_graph(group, conf.colors[i], conf.legend[i], conf.indicator_titles, conf.label_dist_factor)
            i+=1
        legend(scatterpoints=1, loc=conf.legend_loc, fancybox=True)
        return fig


if __name__ == '__main__':
    """
    @deprecated: the visualiser + conf file should be used as a main entry point.
    """
    vis = MultigroupVisualisation()
    fig = vis.draw()
    if conf.write_to_file:
        fig.savefig(conf.filename, format=os.path.splitext(conf.filename)[1][1:])
    else:
        show()
