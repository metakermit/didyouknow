'''
Created on 26. 6. 2012.

@author: kermit
'''
from foc.visualiser.data_organiser.abstract_data_organiser import AbstractDataOrganiser
from dracula.exceptions import NonExistentDataError

class CompleteMultigroupOrganiser(AbstractDataOrganiser):
    '''
    Organises data for a complete multigroup vis.
    (time series with marked model and crises info)
    '''

    def __init__(self):
        AbstractDataOrganiser.__init__(self)

    def _organise_data(self, conf):
        arg = self._extractor.arg()
        arg["country_codes"] = conf.countries
        arg["indicator_codes"] = conf.indicators
        arg["interval"] = (conf.start_date, conf.end_date)
        countries = self._extractor.grab(arg)
        #TODO: add the process method somewhere inside the preprocessor
        #self._extractor.process(conf.process_indicators,
        #                           method = "slope",
        #                           look_back_years=conf.look_back_years)
        print("organiser got back:")
        print(countries)
        
        self.vis_data = []
        for country in countries:
            x_ind_code,y_ind_code = country.indicator_codes()[:2]
            x_ind = country.get_indicator(x_ind_code)
            y_ind = country.get_indicator(y_ind_code)
            years = range(conf.start_date, conf.end_date)
            
            # arrange x and y vectors
            all_x = []
            all_x_dates = []
            all_y = []
            all_y_dates = []
            for t in years:
                try:
                    x = x_ind.get_value_at(t)
                    y = y_ind.get_value_at(t)
                    all_x.append(x)
                    all_x_dates.append(t)
                    all_y.append(y)
                    all_y_dates.append(t)
                except NonExistentDataError:
                    continue
            
            country_repr = {'code': country.code, 'dates': all_x_dates,
                            #'x_ind': x_ind.simple_dict_repr(),
                            #'y_ind': y_ind.simple_dict_repr()}
                            'x_ind': {'code': x_ind.code, 'data': all_x},
                            'y_ind': {'code': y_ind.code, 'data': all_y}}
            self.vis_data.append(country_repr)
        
        return self.vis_data

