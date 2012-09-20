'''
Created on 14. 12. 2011.

@author: kermit
'''
# don't look at these imports...
from foc.forecaster.ai.preprocessor import Preprocessor
# ...now continue reading.

######################################
# FOC Forcaster - configuration file #
######################################

# take data from start_date to end_date
start_date = 1995
end_date = 2000

# see codes at http://en.wikipedia.org/wiki/ISO_3166-1_alpha-3
__countries = """
usa
nor
gbr
"""

# a file that states when did crises occur in countries
sample_selection_file = "./io/crises-imf-banking.xls"

# see codes by selecting the desired indicators at
# http://databank.worldbank.org/
# , downloading the meta-file in excel format
# and copying the codes from the excel table
# or take a look at the last part of the url while browsing
# http://data.worldbank.org/indicator/

# the part after "-" is the description that goes to the graph 
__indicators = """
SP.DYN.LE00.MA.IN-Life expectancy at birth, male (years)
SP.POP.1564.TO.ZS-Percentage ages 15-64 (%)
"""
# population - SP.POP.TOTL
# real interest rate - FR.INR.RINR
# GDP per capita - NY.GDP.PCAP.KD
# unemployment rate - SL.UEM.TOTL.ZS
# GDP growth (annual %) - NY.GDP.MKTP.KD.ZG

# which indicators to apply slope/derivative to
__process_indicators = """
"""

################
# Visualisation options   #
################

# True - graphs written to files
# False - interactive graphs will be shown in a GUI

# choose what kind of time series to draw
# possible arguments are:
# TSV (TimeSeriesVisualisation)
# MV (MultigroupVisualisation)
# CMV (CompleteMultigroupVisualisation)
#
visualisation = "CMV"

# True - all curves plotted on the same graph
# False - each curve plotted in a separate graph
combine_plots = True

write_to_file = False

filename = "./io/viz/viz-complete.svg"

# this will be the graph title if auto_title is False
graph_title = "USA - active population & life expectancy"

# generate the title automatically from country codes...
auto_title = True 
# ...and append this to the end 
title_end = "active population & life expectancy"
# positioning labels next to points...
# -----------------------------------------------
# if dist in pixels, set absolute number of pixels to offset labels
# else use a factor of the distance between last two points 
dist_pixels = True
label_dist_x = -0.3
label_dist_y = 0.5

dist_2d=True
#if above is true, scale labels by 2 dimensions
#else just use the same factor (label_dist_factor_x)
label_dist_factor_x = 1.0
label_dist_factor_y = 1.8

legend_loc = "upper right"
# possible:
#----------
#   right
#	center left
#	upper right
#	lower right
#	best
#	center
#	lower left
#	center right
#	upper left
#	upper center
#	lower center

#############################
# Time-series-specific options
#############################


#############################
# Multigroup-specific options
#############################

# define your groups
__events = """
FIN-1991
*
USA-1988
*
USA-2007
*
LVA-1995
"""

__colors = """
r
b
g
y
"""

__legend="""
crysis
non-crysis
non-crysis
non-crysis
"""
years_before=5
years_after=5

#############################
# Complete-multigroup-specific options
#############################

def model(all_x, all_x_dates, all_y, all_y_dates):
    values = all_x[-(look_back_years+1):-1]
    dates = all_x_dates[-(look_back_years+1):-1]
    ind1 = Preprocessor(dates,values).slope()
    values = all_y[-(look_back_years+1):-1]
    dates = all_y_dates[-(look_back_years+1):-1]
    ind2 = Preprocessor(dates,values).slope()
    return (ind1<0.20 and ind2<0.11)

#def model(ind1, ind2):
#    return (ind1<0.11 and ind2<0.20)

# specify manually when has a crysis ocurred in a country
# list years per country, separated with a *
# UNUSED! The samples selection XLS file is used
__manual_crises = """
1991
*
3000
"""

look_back_years = 3

# see available markers in file "/usr/lib/pymodules/python2.7/matplotlib/markers.py"
crisis_colour = "red"
crisis_mark = "d"
crisis_size = 250
model_true_colour = "orange"
model_true_mark = "^"
model_true_size = 150
model_false_colour = "blue"
model_false_mark = "o"
model_false_size = 10

#############################
# Performance
#############################

# pause in seconds between subsequent World Bank API queries
wb_pause = 0

# save downloaded data to a caching MongoDB database 
cache_enabled = True
# the host that's serving the cache DB
cache_host = "lis.irb.hr"
# and the port
cache_port=27017

########################################################
### INTERNAL STUFF - do not touch or be intimidated by:
########################################################
import re
#pattern = " |\n"
pattern = "\s"
newline = re.compile("[\n\r]")
whitespace = re.compile("\s|\b")
listify = lambda txt : [el.rstrip() for el in re.split(pattern,txt) if el!=""]
listify_int = lambda txt : [int(el.rstrip()) for el in re.split(pattern,txt) if el!=""]
listify_newline = lambda txt : [el.rstrip() for el in newline.split(txt) if el!=""]
listify_no_tails = lambda txt : [el.split("-")[0].rstrip() for el in listify_newline(txt)]
listify_only_tails = lambda txt : [el.split("-", 1)[1].rstrip() for el in listify_newline(txt)]

countries = listify(__countries)
indicators = listify_no_tails(__indicators)
indicators_full = listify_newline(__indicators)
indicator_title_texts = listify_only_tails(__indicators)
indicator_titles = dict([(indicators[i], indicator_title_texts[i]) for i in range(len(indicators))])
process_indicators = set(listify_no_tails(__process_indicators))
groups = [listify(x) for x in __events.split("*")]
colors = listify(__colors)
legend = listify(__legend)
manual_crises = [listify_int(x) for x in __manual_crises.split("*")]
