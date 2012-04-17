'''
Created on 16. 12. 2011.

@author: kermit
'''
from forecaster.sources.extractor import Extractor
import conf

def run():
    extractor = Extractor()
    extractor.fetch_data_per_conf(conf)
    extractor.process(conf.process_indicators)
    extractor.draw()

if __name__ == '__main__':
    run()