'''
Created on 21. 5. 2012.

@author: kermit
'''
from pylab import *
import os

from dracula.extractor import Extractor
from foc.forecaster.common.exceptions import MustOverrideError
from foc.visualiser.data_presenter.ivisualisation import *
#import conf

class IMatplotVis(IVisualisation):
    '''
    Matplotlib visualiser interface with common functions.
    '''
        
    def _add_legend(self):
        legend()
        
    def _should_add_meta_marks(self):
        """
        Tells if additional graph stuff (axis labels, legend)
        should be placed 
        @return: Boolean
        """
        return not conf.combine_plots or self._counter == 0
        
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
            draw()
            #show()
    def _show(self):
        show()
        
