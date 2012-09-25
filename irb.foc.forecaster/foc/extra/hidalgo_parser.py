# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import csv
import pandas as pd
location = "/home/kermit/projekti/lp/foc/trunk/irb.foc.forecaster/io/RCA.txt"
index_tuples = []
values = []
with open(location,"rb") as csv_file:
    raw_data = csv.reader(csv_file, delimiter=" ", skipinitialspace=True)
    stop = 1000
    for line in raw_data:
        #if stop ==0:
        #    break
        stop-=1
        product, country, year = line[0], line[1], int(line[2])
        current_ind = (country, product,year)
        index_tuples.append(current_ind)
        try:
            values.append(float(line[3]))
        except ValueError:
            values.append(None)
multi_index = pd.MultiIndex.from_tuples(index_tuples, names = ["country", "product", "year"])
s = pd.Series(values, index = multi_index)
#print(s[("0010","AUS",1980)])
#s.head(n=100)
#grouped = s.groupby(level="country").mean()
#grouped.head(n=100)
#s.plot()

# <markdowncell>

# Sort the index.

# <codecell>

from pylab import *
s = s.sortlevel(level=0)
#print(s.head(100))
#print(s[("ARG")])
#grouped = s.groupby(level="country")
#grouped[("USA")]
s.index.lexsort_depth

#indicators = s[("USA")]
#indicators["0010"]
#plot(s.head(100))

# <codecell>

s[("USA", "9110")].plot()

