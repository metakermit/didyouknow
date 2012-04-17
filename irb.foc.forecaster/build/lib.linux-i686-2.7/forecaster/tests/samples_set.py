'''
Created on 16. 12. 2011.

@author: kermit
'''
import unittest

from forecaster.ai.samples_set import SamplesSet

class Test(unittest.TestCase):


    def test_build(self):
        look_back_years = 3
        samples_set = SamplesSet(look_back_years)
        samples_set.t_loc = "test_sample_selection.xls"
        train_samples, test_samples = samples_set.build_from_crises_file(["usa", "deu"], ["SP.POP.65UP.TO.ZS"], 0.50)
        self.assertEqual(len(train_samples), 4)
        self.assertEqual(len(test_samples), 3)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_build']
    unittest.main()