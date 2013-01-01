'''
Created on Sep 27, 2012

@author: Matija
'''
import unittest
from dracula.local.rca import api

class Test(unittest.TestCase):


    def test_grabbing(self):
        countries = api.query_multiple_data(country_codes=["USA", "HRV"],
                                           indicator_codes=['0011', '0012', '0013'], start_date=1980, end_date=2010)
        self.assertTrue(len(countries)>1, "must get something")
        expected_values = [0.053304600000000001, 0.064970799999999995, 0.053569400000000003, 0.052973199999999998, 0.13446610000000001, 0.079521999999999995, 0.064925800000000006, 0.15640119999999999, 0.082641199999999998, 0.050845099999999997, 0.12788040000000001, 0.021213200000000001, 0.027366999999999999, 0.055735100000000003, 0.098319500000000004, 0.12376719999999999, 0.059513499999999997]    
        for country in countries:
            if country.code == "USA":
                got_values = country.get_indicator("0013").values
        self.assertTrue(expected_values==got_values, "must get that data over there")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGrabbing']
    unittest.main()