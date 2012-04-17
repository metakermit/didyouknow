'''
Created on 20. 12. 2011.

@author: kermit
'''
import unittest
from forecaster.ai.preprocessor import *

class Test(unittest.TestCase):


    def test_slope(self):
        x = range(1,5)
        y = [1.5, 1.6, 2.1, 3.0]
        pp = Preprocessor(x,y)
        self.assertEqual(pp.slope(), 0.5)
        
    def test_maximum(self):
        x = range(1,5)
        y = [1.5, 3.0, 2.1, 1.6]
        pp = Preprocessor(x,y)
        self.assertEqual(pp.maximum(), (3.0, 1))
        
    def test_minimum(self):
        x = range(1,5)
        y = [1.5, 3.0, 2.1, 1.6]
        pp = Preprocessor(x,y)
        self.assertEqual(pp.minimum(), (1.5, 0))
    
    def test_average(self):
        x = range(1,5)
        y = [1.5, 3.0, 2.1, 1.6]
        pp = Preprocessor(x,y)
        self.assertEqual(pp.average(), 2.05)
        
    def test_slope_na(self):
        x = range(1,5)
        y = [1.5, na, 2.1, 3.0]
        pp = Preprocessor(x,y)
        self.assertEqual(is_na(pp.slope()), True)
        
    def test_maximum_na(self):
        x = range(1,5)
        y = [1.5, na, 2.1, 1.6]
        pp = Preprocessor(x,y)
        self.assertEqual(pp.maximum(), (2.1, 2))
        
    def test_minimum_na(self):
        x = range(1,5)
        y = [na, 3.0, 2.1, 1.6]
        pp = Preprocessor(x,y)
        self.assertEqual(pp.minimum(), (1.6, 3))
    
    def test_average_na(self):
        x = range(1,5)
        y = [1.5, 3.0, na, 1.8]
        pp = Preprocessor(x,y)
        self.assertEqual(pp.average(), 2.1)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_preprocess']
    unittest.main()