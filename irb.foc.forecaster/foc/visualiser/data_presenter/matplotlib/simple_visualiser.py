'''
Created on 26. 6. 2012.

@author: kermit
'''
from foc.visualiser.data_organiser.complete_multigroup import CompleteMultigroupOrganiser
import foc.visualiser.data_presenter.default_vis_conf as conf
from pprint import pprint

def run_matplotlib():
    organiser = CompleteMultigroupOrganiser()
    repr = organiser.get_representation(conf)

if __name__ == '__main__':
    organiser = CompleteMultigroupOrganiser()
    repr = organiser.get_representation(conf)
    pprint(repr)