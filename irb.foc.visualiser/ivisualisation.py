'''
Created on 21. 5. 2012.

@author: kermit
'''
from pylab import *
import os

from forecaster.sources.extractor import Extractor
from forecaster.common.exceptions import MustOverrideError
import conf

class IVisualisation(object):
    '''
    Visualiser interface.
    '''
    
    #_extractor = None
    #figure = None
    
    def __init__(self):
        '''
        Constructor
        '''
        self._extractor = Extractor()
        self._counter = 0
        self._got_items = False
        
    def _add_legend(self):
        legend()
        
    def _should_add_meta_marks(self):
        """
        Tells if additional graph stuff (axis labels, legend)
        should be placed 
        @return: Boolean
        """
        return not conf.combine_plots or self._counter == 0
    
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
        
    def _start_new_figure(self):
        self.figure = figure()
        hold(True)
        suptitle(self.get_title(), fontsize=16)
    
    def _finish_figure(self):
        """
        save or show the figure.
        @param item: optional if you want to combine multiple
        plots so that an individual name can be used 
        """
        self._add_legend()
        if conf.write_to_file: # indeed write to file
            name, extension = os.path.splitext(conf.filename)
            extension = extension[1:]
            if not conf.combine_plots:
                try:
                    ending = str(self._get_items()[self._counter-1]).lower()
                except AttributeError: # except not needed
                    ending = str(self._counter).lower()
                name = name + "-" + ending          
            self.figure.savefig(name + "." + extension, format=extension)
        elif conf.combine_plots or self._counter == len(self._get_items()):
            # we'll just plot it live in a new window
            show()
        
    def _get_items(self):
        """
        Get items that form independent units of data for
        drawing. Normally these are countries, but this can
        be overriden. Each item then gets passed to the
        _create_figure function to draw them on a graph.
        @return: list of items
        """
        if not self._got_items:
            self._extractor.fetch_data(conf.countries, conf.indicators, conf.start_date, conf.end_date)
            self._extractor.process(conf.process_indicators,
                                   method = "slope",
                                   look_back_years=conf.look_back_years)
            self._got_items = True
        countries = self._extractor.get_countries()
        return countries
    
    def _create_figure(self, item):
        """
        Create a figure and return it as a matplotlib object. Must override.
        """
        raise MustOverrideError
    
    def create_all_figures(self):
        """
        Write all figures to file(s) or plot in one or more windows.
        """
        # we create only one figure if this is a combo plot
        if conf.combine_plots:
            self._start_new_figure()
        # iterate through items (e.g. countries)
        other_items = conf.countries
        items = self._get_items()
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
        
