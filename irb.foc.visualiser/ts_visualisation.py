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

    def create(self):
        """
        create single time series line plots for the data defined in the conf file
        """
        self.extractor.fetch_data_per_conf(conf)
        self.extractor.process(conf.process_indicators)
        countries = self.extractor.get_countries()
        # draw
        grid()
        xlabel("year")
        ylabel("value")
        for ind_code in conf.indicators:
            for country in countries:
                indicator = country.get_indicator(ind_code)
                plot(indicator.dates, indicator.values,
                     label = country.code + " - " + indicator.code)
        legend()
        return self.figure

    
    