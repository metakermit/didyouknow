'''
Created on 15. 12. 2011.

@author: kermit
'''
import unittest
from forecaster.model.indicator import Indicator

class Test(unittest.TestCase):


    def test_apply_derivative(self):
        indicator = Indicator(dates=[1,2,3], values=[17,16,13])
        indicator.apply_derivative()
        self.assertEqual(indicator.values, [-1,-3])
        self.assertEqual(indicator.dates, [2,3])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testDerivative']
    unittest.main()