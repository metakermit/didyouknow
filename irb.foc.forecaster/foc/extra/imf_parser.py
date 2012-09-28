# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# Reading data
# ===========
# In this part we'll get the crisis years from a published IMF data set.
# 
# First let's get the standard country codes coresponding to these countries using dracula.

# <codecell>

import inspect
from dracula.extractor import Extractor
import dracula
extractor = Extractor()
country_codes = {}
countries = extractor.grab_metadata("countries")
print(inspect.getsourcelines(dracula.wb.parser.parse_multiple_countries_alone))
for country in countries:
    #print(dir(country))
    country_codes[country.name]=country.code
print(country_codes)

# <markdowncell>

# Manual fixing

# <codecell>

country_codes["Serbia, Republic of"] = 'SRB'
country_codes['Brunei'] = 'BRN'
country_codes[u"Lao People’s Dem. Rep."] = 'LAO'
country_codes['Venezuela'] = 'VEN'
country_codes['Korea'] = 'KOR'
country_codes['Luxemburg'] = 'LUX'
country_codes['Congo, Dem. Rep. of'] = 'COG'
country_codes['Central African Rep.'] = 'CAF'
country_codes['China, P.R.: Hong Kong'] = 'HKG'
country_codes[u'Côte d’Ivoire'] = 'CIV'
country_codes['China, P.R.'] = 'CHN'
country_codes['Macedonia'] = 'MKD'
country_codes['Congo, Rep. of'] = 'COG'
country_codes['Iran, I.R. of'] = 'IRN'
country_codes['Egypt'] = 'EGY'
country_codes[u'São Tomé and Principe'] = 'STP'
country_codes['Yemen'] = 'YEM'
country_codes['Venezuela'] = 'VEN'
country_codes['Russia'] = 'RUS'
country_codes['Luxemburg'] = 'LUX'
country_codes['Gibraltar'] = 'GIB'

# <markdowncell>

# Now, let's get busy reading the IMF data into dictionaries with country codes as keys and years as values.

# <codecell>

import xlrd
def add_crisis(what, where, key):
    #where[key].add(what)
    if what!=None:
        try:
            where[key].add(what)
        except KeyError:
            where[key] = set([what])

def parse_imf_db(loc):
    wb = xlrd.open_workbook(loc)
    sh = wb.sheet_by_index(0)
    banking_crises = {}
    currency_crises = {}
    debt_crises = {}
    problematic = []
    for rownum in range(3,sh.nrows-1):
        country = sh.row_values(rownum)[0].rstrip()
        try:
            code = country_codes[country]
        except KeyError:
            code = country # we'll fix those maunally
            problematic.append(code)
        years = [int(x) if x!="" else None for x in sh.row_values(rownum)[1:]]
        add_crisis(years[0], banking_crises, code)
        add_crisis(years[1], currency_crises, code)
        add_crisis(years[2], debt_crises, code)
        #print(country, years)
    # Test to se there are no problems (should be empty).
    print("Problematic:")
    print(problematic)
    return banking_crises, currency_crises, debt_crises
import os
loc = os.path.expanduser("~/Dropbox/dev/itd/skripte/ipy_notebook/data/imf/IMF Financial crisis episodes database 2008.xls")
banking_crises, currency_crises, debt_crises = parse_imf_db(loc)
print(currency_crises)

# <codecell>

print(currency_crises["DZA"])

# <markdowncell>

# Doing stuff to data
# ===============
# For starters here's my heuristic for generating normal years.

# <codecell>

def pick_normal_years(crisis_years, minimum = 1971, maximum = 2007):
    crisis_years = sort(list(crisis_years))
    normal_years = []
    safe_from_crisis = 10
    if 0<len(crisis_years)<=3:
        # before
        year_before = crisis_years[0]-safe_from_crisis
        while year_before>=minimum:
            normal_years.append(year_before)
            year_before-=safe_from_crisis
        # in between
        for i in range(len(crisis_years)-1):
            if crisis_years[i+1]-crisis_years[i]>=20:
                delta = crisis_years[i+1]-crisis_years[i]
                normal_years.append(crisis_years[i]+int(round(delta/2.0)))
        # after
        year_after = crisis_years[-1]+safe_from_crisis
        while year_after <= maximum:
            normal_years.append(year_after)
            year_after+=safe_from_crisis
    return sort(normal_years)
print(pick_normal_years([1982, 1983, 2004]))
print(pick_normal_years([1983, 1993]))
print(pick_normal_years([2003, 2004]))
print(pick_normal_years([1973, 1974]))

# <markdowncell>

# A function to combine crises

# <codecell>

def combine_crises(crisis_def_list):
    result_crisis_def = {}
    for crisis_def in crisis_def_list:
        for country in crisis_def.keys():
            years = crisis_def[country]
            try:
                result_crisis_def[country]|=years
            except KeyError:
                result_crisis_def[country]=years
    return result_crisis_def
crisis_def_a = {"HRV":set([1998, 2008]), "USA":set([1975, 2009])}
crisis_def_b = {"GBR":set([1979]), "USA":set([2011])}
print(combine_crises([crisis_def_a, crisis_def_b]))

# <markdowncell>

# Writing data
# ===========

# <codecell>

from xlwt import Workbook
def write_datatests(crisis_def_list, location = "./out", suffix = ""):
    book = Workbook()
    sheet1 = book.add_sheet('Sheet 1')
    result_crises = combine_crises(crisis_def_list)
    row_num = 0
    for country_code in sort(result_crises.keys()):
        years = sort(list(result_crises[country_code]))
        try:
            len(years)
        except:
            print(years)
            print(country_code)
        sheet1.write(row_num, 0, country_code)
        crisis_row = sheet1.row(row_num)
        crisis_row.write(1, "crisis")
        for j in range(len(years)):
            crisis_row.write(j+2, years[j])
        normal_row = sheet1.row(row_num+1)
        normal_row.write(1, "normal")
        normal_years = pick_normal_years(years)
        for j in range(len(normal_years)):
            normal_row.write(j+2, normal_years[j])
        row_num+=2
    saveloc = os.path.expanduser(location)+suffix+".xls"
    book.save(saveloc)
location="~/Dropbox/dev/itd/skripte/ipy_notebook/data/imf/crisis-imf-"
write_datatests([banking_crises], location, suffix = "banking")
write_datatests([currency_crises], location, suffix = "currency")
write_datatests([debt_crises], location, suffix = "debt")
write_datatests([banking_crises, currency_crises], location, suffix = "banking+currency")
write_datatests([banking_crises, debt_crises], location, suffix = "banking+debt")
write_datatests([currency_crises, debt_crises], location, suffix = "currency+debt")
write_datatests([banking_crises, currency_crises, debt_crises], location, suffix = "banking+currency+debt")
print("done")

# <markdowncell>

# Parse the new IMF dataset from 2012
# ==============================
# Parse thew new data as dictionaries and write them down.

# <codecell>

def csv_to_years(csv_years):
    if type(csv_years)==float or type(csv_years)==int:
        years = [int(csv_years)]
    else:
        years = list(int(x) for x in csv_years.split(", ") if x!="")
    return years

def add_many_crises(what, where, key):
    #where[key].add(what)
    if what!=[]:
        try:
            where[key] |= set(what) # union with the existing set
        except KeyError:
            where[key] = set(what)

def parse_imf_db_2012(loc):
    wb = xlrd.open_workbook(loc)
    sh = wb.sheet_by_index(1)
    banking_crises = {}
    currency_crises = {}
    debt_crises = {}
    problematic = []
    for rownum in range(2,sh.nrows):
        country = sh.row_values(rownum)[0].rstrip()
        try:
            code = country_codes[country]
        except KeyError:
            code = country # we'll fix those maunally
            problematic.append(code)
        csv_years_all = [x for x in sh.row_values(rownum)[1:4]]
        #years = [int(x) if x!="" else None for x in sh.row_values(rownum)[1:]]
        #print(csv_to_years(csv_years_all[0]))
        #print(sh.row_values(rownum))
        #print(rownum)
        add_many_crises(csv_to_years(csv_years_all[0]), banking_crises, code)
        add_many_crises(csv_to_years(csv_years_all[1]), currency_crises, code)
        add_many_crises(csv_to_years(csv_years_all[2]), debt_crises, code)
        #print(country, years)
    print("PROBLEMATIC:")
    print(problematic)
    return banking_crises, currency_crises, debt_crises
loc = os.path.expanduser("~/Dropbox/dev/itd/skripte/ipy_notebook/data/imf/2012/IMF Financial crisis episodes database 2012.xls")
banking_crises_new, currency_crises_new, debt_crises_new = parse_imf_db_2012(loc)
print(currency_crises_new)

# <codecell>

location = os.path.expanduser("~/Dropbox/dev/itd/skripte/ipy_notebook/data/imf/2012/crisis-imf-2012-")
write_datatests([banking_crises_new], location, suffix = "banking")
write_datatests([currency_crises_new], location, suffix = "currency")
write_datatests([debt_crises_new], location, suffix = "debt")
write_datatests([banking_crises_new, currency_crises_new], location, suffix = "banking+currency")
write_datatests([banking_crises_new, debt_crises_new], location, suffix = "banking+debt")
write_datatests([currency_crises_new, debt_crises_new], location, suffix = "currency+debt")
write_datatests([banking_crises_new, currency_crises_new, debt_crises_new], location, suffix = "banking+currency+debt")

# <markdowncell>

# Find deltas...

# <codecell>

def find_delta(crisis_def, crisis_def_new):
    crisis_def_delta = {}
    for country in crisis_def_new:
        years_new = crisis_def_new[country]
        try:
            years_old = crisis_def[country]
        except KeyError:
            years_old = set()
        added_years = years_new - years_old
        if len(added_years)>0:
            crisis_def_delta[country] =  added_years
    return crisis_def_delta
crisis_def_a = {"HRV":set([1998, 2008]), "USA":set([1975, 2009])}
crisis_def_b = {"GBR":set([1979]), "USA":set([1975, 2009,2011]), "HRV":set([1998, 2008])}
print(find_delta(crisis_def_a, crisis_def_b))

# <codecell>

banking_crises_delta = find_delta(banking_crises, banking_crises_new)
currency_crises_delta = find_delta(currency_crises, currency_crises_new)
debt_crises_delta = find_delta(debt_crises, debt_crises_new)
print(banking_crises_delta)
write_datatests([banking_crises_delta], location, suffix = "delta-banking")
write_datatests([currency_crises_delta], location, suffix = "delta-currency")
write_datatests([debt_crises_delta], location, suffix = "delta-debt")
write_datatests([banking_crises_delta, currency_crises_delta], location, suffix = "delta-banking+currency")
write_datatests([banking_crises_delta, debt_crises_delta], location, suffix = "delta-banking+debt")
write_datatests([currency_crises_delta, debt_crises_delta], location, suffix = "delta-currency+debt")
write_datatests([banking_crises_delta, currency_crises_delta, debt_crises_delta], location, suffix = "delta-banking+currency+debt")

