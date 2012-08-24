'''
Created on 22. 8. 2012.

@author: kermit
'''
import unittest

from dracula.extractor import Extractor

class Test(unittest.TestCase):
    
    def test_extractor(self):
        extractor = Extractor()
        countries = extractor.grab()
        self.assertTrue(len(countries)>0)

        arg = extractor.arg()
        arg["country_codes"] = ["usa", "hrv"]
        arg["indicator_codes"] = ["SP.POP.TOTL", "SL.TLF.PART.MA.ZS"]
        arg["interval"] = (2005, 2006)
        countries = extractor.grab(arg)
        self.assertTrue(len(countries)>0)
        
        arg = extractor.arg()
        arg["country_codes"] = ["hrv"]
        arg["indicator_codes"] = ["SP.POP.TOTL"]
        arg["interval"] = (1998, 1999)
        countries = extractor.grab(arg)
        indicator = countries[0].get_indicator("SP.POP.TOTL")
        #print indicator.get_values()
        self.assertEqual(indicator.values, [4501000.0, 4554000.0])
        self.assertEqual(indicator.dates, [1998, 1999])
        
    def test_cache(self):
        extractor = Extractor()
        extractor.enable_cache('lis.irb.hr', 27017)
        countries = extractor.grab()
        self.assertEqual(extractor.is_cached(extractor.arg()), True,
                         "Countries must be cached after grab")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testExtractor']
    unittest.main()