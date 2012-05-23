'''
Created on 22. 5. 2012.

@author: kermit
'''

import math

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
        
        #country = conf.countries[0]
        countries = self.extractor.fetch_data(conf.countries, conf.indicators, conf.start_date, conf.end_date)
        i = 0
        for country in countries:
            crisis_years = set(conf.manual_crises[i])
            i = i +1
            x_ind_code,y_ind_code = country.indicator_codes()[:2]
            x_ind = country.get_indicator(x_ind_code)
            y_ind = country.get_indicator(y_ind_code)
            years = range(conf.start_date, conf.end_date)
            all_x = []
            all_x_dates = []
            all_y = []
            all_y_dates = []
            labeled_crisis, labeled_model, labeled_outside_model = False, False, False
            for t in years:
                try:
                    x = x_ind.get_value_at(t)
                    y = y_ind.get_value_at(t)
                    all_x.append(x)
                    all_x_dates.append(t)
                    all_y.append(y)
                    all_y_dates.append(t)
                    xlabel(conf.indicator_titles[x_ind_code])
                    ylabel(conf.indicator_titles[y_ind_code])
                    legend_label = None
                    if t in crisis_years:
                        label_text = "Crisis: " + str(t)
                        dist = math.sqrt(math.pow(x-x_ind.get_value_at(t-1),2)
                                         +math.pow(y-y_ind.get_value_at(t-1),2))*conf.label_dist_factor
                        annotate(label_text, size="medium" , xy=(x+dist,y+dist))
                        mark = conf.crisis_mark
                        colour = conf.crisis_colour
                        size = conf.crisis_size
                        if not labeled_crisis: legend_label, labeled_crisis = "crisis", True
                    else:
                        if len(all_x)>3 and conf.model(all_x, all_x_dates, all_y, all_y_dates):
                            colour = conf.model_true_colour
                            mark = conf.model_true_mark
                            size = conf.model_true_size
                            if not labeled_model: legend_label, labeled_model = "satisfies model", True
                        else:
                            colour = conf.model_false_colour
                            mark = conf.model_false_mark
                            size = conf.model_false_size
                            if not labeled_outside_model: legend_label, labeled_outside_model = "doesn't satisfy model", True
                    scatter(x, y, s=size, c=colour,
                            alpha=1.0, marker=mark, label = legend_label)
                except NonExistentDataError:
                    pass
            if len(all_x)!=len(all_y): # there is no data for one of the indicators
                print("Error: number of data points to be plotted not equal")
                raise NonExistentDataError
            try:
                plot(all_x,all_y, c="black")
            except ValueError:
                print "Something wrong with data to be plotted"
                raise
        
        legend(scatterpoints=1, loc=conf.legend_loc, fancybox=True)
        return self.figure

        
    