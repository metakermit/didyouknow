import unittest

from didyouknow import wb

class Test(unittest.TestCase):
	cro = wb.Country("Croatia")
	usa = wb.Country("USA")
	cro.plot()
	usa.plot()
	self.assertEqual(True, False)