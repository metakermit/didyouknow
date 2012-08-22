'''
Created on 22. 8. 2012.

@author: kermit
'''
import wb.api

def arg():
    arg = {"country_codes" : ["hrv", "usa"],
           "indicator_codes" : ["SP.POP.TOTL"],
           "start_date":1980,
           "end_date":2010}
    return arg

def grab(arg=arg(), api=wb.api):
    #TODO: think about using kwargs
    """
    possible args are:
    
    1) the default one defined in arg()
            {"country_codes" : ["hrv", "usa"],
               "indicator_codes" : ["SP.POP.TOTL"],
               "start_date":1980,
               "end_date":2010}
    2) using interval to set the dates more quickly (overrides start/end_date)
            {"country_codes" : ["hrv", "usa"],
               "indicator_codes" : ["SP.POP.TOTL"],
               "interval":(1980,2010)}
    """
    if "interval" in arg:
        arg["start_date"], arg["end_date"] = arg["interval"]
    countries = api.query_multiple_data(
                                           arg["country_codes"], arg["indicator_codes"],
                                           arg["start_date"], arg["end_date"])
    return countries