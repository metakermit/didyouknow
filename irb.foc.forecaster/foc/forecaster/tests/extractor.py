'''
Created on 16. 12. 2011.

@author: kermit
'''
import unittest

from foc.forecaster.sources.extractor import Extractor
from foc.forecaster.common import conf

class Test(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.extractor = Extractor()


    def test_fetch_data(self):
        countries = self.extractor.fetch_data(["usa", "hrv"], ["SP.POP.TOTL", "SL.TLF.PART.MA.ZS"], 2005, 2006, 0)
        self.assertTrue(len(countries)>0)
        
    def test_fetch_indicator(self):
        indicator = self.extractor.fetch_indicator("hrv", "SP.POP.TOTL", 1998, 1999)
        #print indicator.get_values()
        self.assertEqual(indicator.get_values(), [4501000.0, 4554000.0])
        self.assertEqual(indicator.get_dates(), [1998, 1999])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_fetch_data']
    unittest.main()