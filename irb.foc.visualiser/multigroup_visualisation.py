'''
Created on 8. 2. 2012.

@author: kermit
'''
from pylab import *
import math

from forecaster.sources.extractor import Extractor
import conf
from forecaster.common.exceptions import NonExistentDataError
from ivisualisation import IVisualisation 

import os

class MultigroupVisualisation(IVisualisation):
    """
    A time series marked with crisis and model data
    plotted in a space of two indicators
    (time depicted through point size) 
    """

    def _get_items(self):
        """
        get a list of groups
        """
        return conf.groups
    
    def _auto_graph_title(self):
        if conf.combine_plots:
            item_repr = ", ".join([("(" +
                                    ", ".join([subitem for subitem in item])
                                    + ")").upper() for item in self._get_items()])
        else:
            item_repr = ", ".join(self._get_items()[self._counter]).upper()
        title = "%s - %s" % (item_repr, conf.title_end) 
        return title
    
    def fetch_event_data(self, country_code, start, end):
        """
        get data for a single event
        """
        countries = self._extractor.fetch_data([country_code], conf.indicators, start, end, conf.wb_pause)
        self._extractor.process(conf.process_indicators)
        return countries[0]
    
    def _add_legend(self):
        legend(scatterpoints=1, loc=conf.legend_loc, fancybox=True)
    
    def _add_to_graph(self, group, color, legend_label, indicator_titles, label_dist_factor):
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
            
    
    def _create_figure(self, unit):
        """
        _create_figure a time series marked with crisis and model data
        for the data defined in the conf file
        @param unit: a group object
        """
#        if not conf.combine_plots:
#            warnings.warn("Multigroup doesn't work with uncombined plots")
#            conf.combine_plots = True
        group = unit
        # we're at the group no. self._counter
        i = self._counter
        self._add_to_graph(group, conf.colors[i], conf.legend[i], conf.indicator_titles, conf.label_dist_factor_x)
        return self.figure

if __name__ == '__main__':
    """
    @deprecated: the visualiser + conf file should be used as a main entry point.
    """
    vis = MultigroupVisualisation()
    fig = vis._create_figure()
    if conf.write_to_file:
        fig.savefig(conf.filename, format=os.path.splitext(conf.filename)[1][1:])
    else:
        show()
