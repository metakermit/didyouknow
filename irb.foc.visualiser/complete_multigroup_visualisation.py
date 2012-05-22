'''
Created on 22. 5. 2012.

@author: kermit
'''
from ivisualisation import *
from multigroup_visualisation import MultigroupVisualisation
import conf
from forecaster.common.exceptions import NonExistentDataError

class CompleteMultigroupVisualisation(MultigroupVisualisation):
    '''
    Multigroup that shows all the years and marks certain
    parts of the line
    '''

    def __init__(self):
        '''
        Constructor
        '''
        IVisualisation.__init__(self)
        self.model = conf.model

    def create(self):
        """
        create a time series marked with crisis and model data
        for the data defined in the conf file
        """
        suptitle(conf.graph_title, fontsize=16)
        #grid()
        #colors = ["r","b","g","y"]
        
        country = conf.countries[0]
        countries = self.extractor.fetch_data([country], conf.indicators, conf.start_date, conf.end_date)
        
        
        #legend(scatterpoints=1, loc=conf.legend_loc, fancybox=True)
        return self.figure

        
    