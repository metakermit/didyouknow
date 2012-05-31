'''
Created on 21. 5. 2012.

@author: kermit
'''
from ivisualisation import *
import conf

class TimeSeriesVisualisation(IVisualisation):
    '''
    Line plots of simple time series data
    '''

    def __init__(self):
        '''
        Constructor
        '''
        IVisualisation.__init__(self)

    def _create_figure(self, item):
        """
        Draw all the indicators on the graph for
        a given country.
        @param item: a country object
        """
        country = item
        # draw
        grid()
        if self._should_add_meta_marks(): 
            xlabel("Year")
            ylabel("Value")
        for ind_code in conf.indicators:
            indicator = country.get_indicator(ind_code)
            plot(indicator.dates, indicator.values, label =
                 country.code + " - " + indicator.code)
        return self.figure
        
    def _create_figure_old(self):
        """
        _create_figure single time series line plots for the data defined in the conf file
        @deprecated: used before ivisualisation existed
        """
        self._extractor.fetch_data_per_conf(conf)
        self._extractor.process(conf.process_indicators)
        countries = self._extractor.get_countries()
        # draw
        grid()
        xlabel("year")
        ylabel("value")
        for ind_code in conf.indicators:
            for country in countries:
                indicator = country.get_indicator(ind_code)
                plot(indicator.dates, indicator.values,
                     label = country.code + " - " + indicator.code)
        #legend()
        return self.figure

    
    