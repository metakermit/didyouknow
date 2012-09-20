'''
Created on 5. 4. 2012.

@author: kermit
'''

from model import Indicator, Country
#TODO: Maybe transfer parsing logic to this class

'''
This module parses World Bank API responses.
'''

def parse_single_country(data_list, nominal_start=None, nominal_end=None):
    """
    @return: single indicator, belonging to one country
    """
    values=[]
    dates=[]
    # sort the list by date
    data_list.sort(key = lambda element : element['date'])
    # parse each element into more precise data structures
    for element in data_list:
        try:
            value = float(element["value"])
            date = int(element["date"])
        except TypeError: # value wasn't a float 
            pass
        else:
            values.append(value)
            dates.append(date)
    #pprint(dates)
    #pprint(values)
    code = data_list[0]['indicator']['id']
    indicator = Indicator(code, dates, values, nominal_start, nominal_end)
    return indicator

def parse_multiple_countries(data_list, nominal_start=None, nominal_end=None):
    """
    @param nominal_start: what start year did the query ask for (not necessarily get)
    @param nominal_end: what end year did the query ask for (not necessarily get)
    @return: list of countries
    """
    #get_country_id = lambda item : item['country']['id']
    # When it's a list of indicator the World bank returns ISO2 codes labeled 'id'
    get_country_id_iso2 = lambda item : item['country']['id']
    countries = []
    #data_list.sort(key = get_country_id)
    while len(data_list)>0:
        current_id_iso2 = get_country_id_iso2(data_list[0])
        country_data = filter(lambda item : get_country_id_iso2(item) == current_id_iso2, data_list)
        # we now basically don't know the country's "real" (iso3) id
        country = Country("")
        country.code_iso2=current_id_iso2
        indicator = parse_single_country(country_data, nominal_start, nominal_end)
        country.set_indicator(indicator)
        countries.append(country)
        # remove parsed data from the list
        #TODO: data_list.remove(i)
        data_list = [item for item in data_list if item not in country_data]
    return countries

def parse_multiple_countries_alone(data_list):
    """
    Parse a query for countries without indicators
    @return: list of countries
    """
    get_country_id = lambda item : item['id']
    get_country_id_iso2 = lambda item : item['iso2Code']
    countries = []
    data_list.sort(key = get_country_id)
    for item in data_list:
        current_id = get_country_id(item)
        current_id_iso2 = get_country_id_iso2(item)
        country = Country(current_id)
        country.code_iso2 = current_id_iso2
        countries.append(country)
    return countries

def add_indicators_to_countries(countries, country_indicators):
    """
    Adds indicators stored in Country objects to a main list of countries 
    """
    old_countries = {}
    # we declare the main list of countries as "old countries" that we will
    # actually keep and want to go through all the "new countries" and add their
    # indicators to the "old ones"
    for country in countries: # we store the main list of countries to a dictionary for quicker access 
        old_countries[country.code_iso2]=country
    for country_list in country_indicators:
        for new_country in country_list:
            # the iso2 code is all we know for the data we got after fetching indicators
            old_country = old_countries[new_country.code_iso2]
            new_ind_code = new_country.indicator_codes[0]
            old_country.set_indicator(new_country.get_indicator(new_ind_code))

def format_country_codes(codes):
    """
    @param codes: list of codes
    @return: list of 2-letter upper-case country codes
    """
    if codes[0]=="all" or codes[0]=="ALL":
        return codes
    for code in codes:
        pass
    return codes
