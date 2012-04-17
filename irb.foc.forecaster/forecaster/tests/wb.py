'''
Created on 15. 12. 2011.

@author: kermit
'''
import unittest

from forecaster.sources import wb

class Test(unittest.TestCase):

    def test_query_multiple_data(self):
        countries = wb.query_multiple_data(country_codes=["usa", "hrv"],
                                           indicator_codes=['SP.POP.TOTL'])
        self.assertTrue(len(countries)>1, "")
    
#    def test_all_indicators(self):
#        inds = wb.all_indicators()
#        self.assertTrue(len(inds)>0, "didn't fetch all indicators")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_all_indicators']
    unittest.main()