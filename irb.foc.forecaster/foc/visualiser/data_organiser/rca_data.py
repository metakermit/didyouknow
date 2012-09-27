'''
Created on 25. 9. 2012.

@author: Matija Piskorec
'''

from dracula.exceptions import NonExistentDataError
from csv import reader
from pandas import MultiIndex, Series

class RCADataOrganiser(object):
    '''
    TODO: Abandon! Move everything to scatter_matrix!
    '''

    def __init__(self):
        location = "io/RCA.txt"
        index_tuples = []
        values = []
        with open(location,"rb") as csv_file:
            raw_data = reader(csv_file, delimiter=" ", skipinitialspace=True)
            for line in raw_data:
                product, country, year = line[0], line[1], int(line[2])
                current_ind = (country,product,year)
                index_tuples.append(current_ind)
                try:
                    values.append(float(line[3]))
                except ValueError:
                    values.append(None)
        multi_index = MultiIndex.from_tuples(index_tuples, names = ["country", "product", "year"])
        s = Series(values, index = multi_index)
        # Sorting is important in order for multiple indexing to work properly!
        s = s.sortlevel(level=0) # Sort by first column.

    def get_rca_data(self, rcaIndicators):
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
        
        values = []
        
        for country in countries:
            years = range(conf.start_date, conf.end_date)
                
            all_x = []
            for t in years:
                x = {}

                x['country'] = country.code
                x['date'] = t
                x['crisis'] = t in crisis_years
                emptyIndicators = 0
                for indicator_code in country.indicator_codes:
                    indicator = country.get_indicator(indicator_code)
                    try:
                        x[indicator_code] = indicator.get_value_at(t)      
                    except NonExistentDataError:
                        x[indicator_code] = ""
                        emptyIndicators = emptyIndicators + 1
                if (len(country.indicator_codes)==emptyIndicators): continue
                all_x.append(x)

            values = values + all_x
        
        self.vis_data = {'countries': conf.countries, 'indicators': conf.indicators, 'values': values}
        
        #return self.vis_data
        return {}

