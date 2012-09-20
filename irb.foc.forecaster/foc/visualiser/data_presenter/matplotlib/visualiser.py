'''
Created on 16. 12. 2011.

@author: kermit
'''

from foc.visualiser.data_presenter import vis_conf as conf
#from ts_visualisation import TimeSeriesVisualisation
#from multigroup_visualisation import MultigroupVisualisation
from complete_multigroup_visualisation import CompleteMultigroupVisualisation
from foc.forecaster.common.exceptions import ConfigurationFileError
from foc.visualiser.data_organiser.complete_multigroup import CompleteMultigroupOrganiser
#===============================================================================
# 
# 
# def draw_time_series():
#    """
#    create single time series line plots for the data defined in the conf file
#    """
#    extractor = Extractor()
#    extractor.fetch_data_per_conf(conf)
#    extractor.process(conf.process_indicators)
#    extractor.create()
#===============================================================================
class Visualiser():
    def __init__(self):
        pass
    
    def get_workers(self):
        vis_str = conf.visualisation
        if vis_str == "TSV":
            #visualisation = TimeSeriesVisualisation()
            raise NotImplementedError
        elif vis_str == "MV":
            #visualisation = MultigroupVisualisation()
            raise NotImplementedError
        elif vis_str == "CMV":
            organiser = CompleteMultigroupOrganiser()
            visualisation = CompleteMultigroupVisualisation()
        else:
            raise ConfigurationFileError
        return organiser, visualisation
    
    def draw(self):
        """
        Entry point to the visualiser. Call visualisation method to get the figure and create it (in a file or live). 
        """
        self.organiser, self.visualisation = self.get_workers()
        self.vis_data = self.organiser.get_representation()
        self.visualisation.create_all_figures(self.vis_data)
    
    def show(self):
        """
        If it's an interactive plot, this will block the code to show the graph
        """
        self.visualisation.show()

if __name__ == '__main__':
    visualiser = Visualiser()
    visualiser.draw()
    