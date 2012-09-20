'''
Created on 27. 6. 2012.

@author: kermit
'''
import os

import foc.visualiser.data_presenter.vis_conf as conf
from foc.forecaster.common.exceptions import MustOverrideError
from dracula.extractor import Extractor

class IVisualisation(object):
    '''
    Abstract visualisation,
    independent of concrete
    implementations.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._counter = 0
        self._got_items = False
        # initialize default configuration options
        
        #TODO: IVisualisation shouldn't use the extractor at all, but rely on a data organiser
        self._extractor = Extractor()
        if conf.cache_enabled:
            self._extractor.enable_cache(conf.cache_host, conf.cache_port)
        
    def get_conf(self):
        return self.conf
        
    def _should_add_meta_marks(self):
        """
        Tells if additional graph stuff (axis labels, legend)
        should be placed 
        @return: Boolean
        """
        return not self.conf.combine_plots or self._counter == 0
    
    def get_title(self):
        if conf.auto_title:
            return self._auto_graph_title()
        else:
            return conf.graph_title
        
    def _auto_graph_title(self):
        if conf.combine_plots:
            country_representation = ", ".join([str(item).upper() for item in self._get_items()])
        else:
            country_representation = str(self._get_items()[self._counter]).upper()
        title = "%s - %s" % (country_representation, conf.title_end) 
        return title
        
    def _get_items(self):
        """
        Get items that form independent units of data for
        drawing. Normally these are countries, but this can
        be overriden. Each item then gets passed to the
        _create_figure function to draw them on a graph.
        @return: list of items
        """
        #TODO: this should just get a data list from the data organiser
        if not self._got_items:
            arg = self._extractor.arg()
            arg["country_codes"] = conf.countries
            arg["indicator_codes"] = conf.indicators
            arg["interval"] = (conf.start_date, conf.end_date)
            self.countries = self._extractor.grab(arg)
            #TODO: preprocessor
#            self._extractor.process(conf.process_indicators,
#                                   method = "slope",
#                                   look_back_years=conf.look_back_years)
            if conf.cache_enabled and self._extractor.was_cached():
                print("Cache was hit, didn't have to query the World Bank API.")
            elif conf.cache_enabled:
                print("Data wasn't cached, queried the World Bank API.")
            self._got_items = True
        return self.countries
    
    def _start_new_figure(self):
        """ a hook for doing pre-plot stuff """
        raise MustOverrideError
    
    def _finish_figure(self):
        """ a hook for doing post-plot stuff """
        raise MustOverrideError
    
    def _create_figure(self, item):
        """
        Create a figure and return it as a matplotlib object. Must override.
        """
        raise MustOverrideError
    
    def _show(self):
        """ a hook to actually show the graph (potentially blocking code)"""
        pass
    
    def show(self):
        if not conf.write_to_file: # interactive
            self._show()
    
    def create_all_figures(self, vis_data):
        """
        Write all figures to file(s) or plot in one or more windows.
        """
        # we create only one figure if this is a combo plot
        if conf.combine_plots:
            self._start_new_figure()
        # iterate through items (e.g. countries)
        #TODO: actually use vis_data here and
        # in the complete_multigroup_visualisation
        for item in self._get_items():
            if not conf.combine_plots:
                self._start_new_figure()
            self._create_figure(item)
            # this counter is important for subclasses. Be careful!
            self._counter += 1
            if not conf.combine_plots:
                self._finish_figure()
        # store the plots in case this is a combined plot 
        if conf.combine_plots:
            self._finish_figure()
        
