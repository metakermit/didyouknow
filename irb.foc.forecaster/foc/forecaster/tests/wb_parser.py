'''
Created on 15. 12. 2011.

@author: kermit
'''
import unittest

from forecaster.sources import wb_parser
from forecaster.model.indicator import Indicator
from forecaster.model.country import Country

class Test(unittest.TestCase):

    def test_add_indicators_to_countries(self):
        c01=Country("country1")
        c01.code_iso2="c1"
        c02=Country("country2")
        c02.code_iso2="c2"
        countries = [c01,c02]
        ind1=Indicator("ind1", [1,2], [10,20])
        ind2=Indicator("ind2", [1,2], [20,30])
        c1 = Country("")
        c1.code_iso2="c1"
        c1.set_indicator(ind1)
        c11 = Country("")
        c11.code_iso2="c1"
        c11.set_indicator(ind2)
        ind3=Indicator("ind1", [1,2], [230,240])
        ind4=Indicator("ind2", [1,2], [330,340])
        c2 = Country("")
        c2.code_iso2="c2"
        c2.set_indicator(ind3)
        c22 = Country("")
        c22.code_iso2="c2"
        c22.set_indicator(ind4)
        countries1 = [c1, c2]
        countries2 = [c11, c22]
        country_indicators = [countries1, countries2]
        wb_parser.add_indicators_to_countries(countries, country_indicators)
        self.assertEqual(len(countries), 2)
        self.assertEqual(len(countries[0].get_indicator("ind1").get_values()), 2)
    
#    def test_all_indicators(self):
#        inds = wb.all_indicators()
#        self.assertTrue(len(inds)>0, "didn't fetch all indicators")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_all_indicators']
    unittest.main()