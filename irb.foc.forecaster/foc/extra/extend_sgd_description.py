#!/usr/bin/python

import sys
import fileinput
from dracula.extractor import Extractor

if __name__=="__main__":
    try:
        desc_path = sys.argv[1]
    except:
        print("Usage:\npython extend_sgd_description.py <desired .sgd_description file>")
        exit()

    extractor = Extractor()
    country_names = {}
    countries = extractor.grab_metadata("countries")
    for country in countries:
        country_names[country.code]=country.name

    for line in fileinput.input(desc_path, inplace = 1):
        num_country, year = (line.rstrip().split("-"))
        number, country_code = num_country.split(" ")
        try:
            country_name = country_names[country_code]
        except:
            country_name = "????"
        sys.stdout.write("%s %s-%s-%s\n" % (number, country_code, year, country_name))
