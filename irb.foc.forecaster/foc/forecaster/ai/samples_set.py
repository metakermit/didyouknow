'''
Created on 16. 12. 2011.

@author: kermit
'''
from forecaster.common import conf
from forecaster.ai.input import Input
from forecaster.sources.extractor import Extractor
from forecaster.ai.sample import *
from forecaster.ai.preprocessor import Preprocessor

from random import sample
from forecaster.common.exceptions import NonExistentDataError
from forecaster.ai.metadata import Metadata

class SamplesSet(object):
    '''
    Responsible for building train and test sets
    '''


    def __init__(self, look_back_years):
        '''
        Constructor
        '''
        self.t_loc = conf.sample_selection_file
        self.extractor = Extractor()
        self.look_back_years = look_back_years
        self.preprocessor = Preprocessor()
        # sample set placeholders
        self.crisis_samples = []
        self.normal_samples = []
        self.metadata = Metadata(conf, look_back_years)
    
#    def buil_per_conf(self):
#        self.build_from_crises_file_from_crises_file(True)
#        pass
       
    def interesting_years_before(self, target_year):
        return range(target_year-self.look_back_years, target_year)
    
    def assign_samples(self, indicators, event_years, event_class, country_code="?"):
        # method creates machine learning samples from indicators
        # arguments:
        # event_years - years of crises or normal periods
        # (as specified in the sample selection file or in a rule)
        # classification - desired class corresponding to these years
        samples = []
        # select only interesting values from the indicator
        for event_year in event_years:
            interesting_years = self.interesting_years_before(event_year)
            try:
                features = []
                for indicator in indicators:
                    new_features = self.preprocessor.preprocess_indicator(indicator,
                                                                          interesting_years)
                    features.extend(new_features)
                sample_description = country_code.upper() + "-" + str(event_year)
                sample = Sample(features, event_class,
                                description=sample_description)
                samples.append(sample)
            except NonExistentDataError:
                pass
        return samples
    
    def convert_to_boundaries(self, event_years, look_back_years):
        """
        convert a list of event years and look back years into
        a list of 2-tuples of boundaries (begin_year, end_year)
        """
        boundaries = []
        for event_year in event_years:
            boundaries.append((event_year-look_back_years, event_year-1))
        return boundaries
    
    def events_to_boundaries(self, all_events, look_back_years):
        event_boundaries = {}
        for key, value in all_events.items():
            event_boundaries[key] = self.convert_to_boundaries(value, look_back_years)
        return event_boundaries    
    
    def combine_events(self, t_crises, t_normal):
        all_events = {}
        for key in t_crises:
            years = []
            years.extend(t_crises[key])
            years.extend(t_normal[key])
            all_events[key]=years
        return all_events
            
    def divide_single(self, samples, test_percentage):
        # divide a list of samples to train and test samples
        if test_percentage==0:
            train_samples = samples
            test_samples = []
        else:
            number_test =int(len(samples)*test_percentage)
            test_samples = sample(samples, number_test)
            train_samples = list(set(samples).difference(set(test_samples)))
        return train_samples, test_samples 
        
    def divide(self, crisis_samples, normal_samples, test_percentage):
        # same as divide_simple, only does that for both crisis and normal samples and combines them
        # into single train and test lists
        self.train_samples, self.test_samples = self.divide_single(crisis_samples, test_percentage)
        new_train_samples, new_test_samples = self.divide_single(normal_samples, test_percentage)
        self.train_samples.extend(new_train_samples)
        self.test_samples.extend(new_test_samples)
        return self.train_samples, self.test_samples
        
    
    def build_from_crises_file(self, country_codes, feature_indicators, test_percentage, sparse=True):
        """
        Entry method that builds a samples set by fetching the data using the extractor.
        Classes are determined from a crisis XLS file.
        
        sparse - if True it fetches the data for the necessary years only.
        """
        # clear the sample sets
        self.crisis_samples = []
        self.normal_samples = []
        # get the years classified as crises / normal periods
        dates_input= Input()
        t_crises, t_normal = dates_input.parse_sample_selection(self.t_loc)
        crises_list, normal_list = dates_input.parse_sample_selection_to_list(self.t_loc)
        # download the data from the World Bank
        if sparse:
            # we fetch only what we need
            # all the events combined - important so that we can only download data near those years
            events = self.combine_events(t_crises, t_normal)
            event_boundaries = self.events_to_boundaries(events,                                                         
                                                         conf.look_back_years)
            countries = self.extractor.fetch_data_sparse(country_codes,
                                                         feature_indicators,
                                                         event_boundaries,
                                                         conf.wb_pause)
        else:
            # we fetch all the data first
            # boundaries
            start_date = min(min(crises_list), min(normal_list))-conf.look_back_years
            end_date = max(max(crises_list), max(normal_list))
            countries = self.extractor.fetch_data(country_codes,
                                                  feature_indicators,
                                                  start_date,
                                                  end_date,
                                                  conf.wb_pause)
        # assign the samples
        for country in countries:
            # fetch all the indicators for target country
            indicators = []
            for ind_code in feature_indicators:
                indicator = country.get_indicator(ind_code)
                indicators.append(indicator)
            # create samples from those indicators - in crises...
            crisis_years = t_crises[country.code]
            new_samples = self.assign_samples(indicators,
                                              crisis_years,
                                              CRISIS_CLASS,
                                              country.code)
            self.crisis_samples.extend(new_samples)
            # ... and in normal periods
            normal_years = t_normal[country.code]
            new_samples = self.assign_samples(indicators,
                                              normal_years,
                                              NORMAL_CLASS,
                                              country.code)
            self.normal_samples.extend(new_samples)
        return self.divide(self.crisis_samples, self.normal_samples, test_percentage)
            
    def build_by_condition(self, country_codes, indicators, feature_indicators, test_percentage):
        # determine crises according to some condition/rule
        raise NotImplemented