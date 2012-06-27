'''
Created on 26. 6. 2012.

@author: kermit
'''
from foc.visualiser.data_organiser.abstract_data_organiser import AbstractDataOrganiser

class CompleteMultigroupOrganiser(AbstractDataOrganiser):
    '''
    Organises data for a complete multigroup vis.
    (time series with marked model and crises info)
    '''

    def __init__(self):
        AbstractDataOrganiser.__init__(self)

    def _organise_data(self, conf):
        self._extractor.fetch_data(conf.countries, conf.indicators, conf.start_date, conf.end_date)
        self._extractor.process(conf.process_indicators,
                                   method = "slope",
                                   look_back_years=conf.look_back_years)
        countries = self._extractor.get_countries()
        
        repr = []
        for country in countries:
            x_ind_code,y_ind_code = country.indicator_codes()[:2]
            x_ind = country.get_indicator(x_ind_code)
            y_ind = country.get_indicator(y_ind_code)
            years = range(conf.start_date, conf.end_date)
            country_repr = {'code': country.code, 'dates': years,
                            'x_ind': x_ind.simple_dict_repr(),
                            'y_ind': y_ind.simple_dict_repr()}
            repr.append(country_repr)
        
        return repr

