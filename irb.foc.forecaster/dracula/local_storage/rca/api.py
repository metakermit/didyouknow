'''
Created on Sep 26, 2012

@author: Matija
'''
from foc.forecaster.common import conf
from pandas import MultiIndex, Series
import numpy as np
from csv import reader
from dracula.model import Country, Indicator

def initial_read():
    print "Initializing RCA _data..."
    
    #location = "io/RCA.txt"
    location = conf.rca_location
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
    
    #s = s.reorder_levels([0,2,1])
    s = s.sortlevel(level=0)
    
    print "Initialization complete!"
    return s

_data = initial_read()

def query_multiple_data(country_codes=['all'], indicator_codes=[], start_date=2010, end_date=2011):
    """
    Perform several queries if necessary to get a multiple indicator tables.
    Parse them and return them as country objects
    @param country_codes: list of country codes to fetch e.g. ['usa','bra']
    @param indicator_codes: list of indicator codes to fetch
    @param start_date: a year from which indicator_codes that we want to fetch should start
    @param end_date: a year from which indicator_codes that we want to fetch should end
    @param pause: a pause in number of seconds between two queries (to ease the load on the World Bank API); unused in this method
        
    @return: a list of country objects
    """
    countries = []
    for country_code in country_codes:
        country_data = _data[str(country_code.upper())]
        country = Country(country_code)
        for indicator_code in indicator_codes:
            indicator_data_full = country_data[indicator_code]
            #indicator_data = indicator_data_full[start_date:end_date]
            wanted_years = np.arange(start_date,end_date)
            indicator_data = indicator_data_full.ix[wanted_years].dropna()
            dates=list(indicator_data.index)
            values=list(indicator_data.values)
            indicator = Indicator(code=indicator_code, dates=dates, values=values, nominal_start=start_date, nominal_end=end_date)
            country.set_indicator(indicator)
        countries.append(country)
    return countries

def all_indicators():
    _data
    indicators = list(_data.groupby(level="product").index.keys())
    return indicators


#print query_multiple_data(["USA","BRA"],["0010","0011"],1980,1990)
print "Fetching _data..."
print _data