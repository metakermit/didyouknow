'''
Created on 14. 12. 2011.

@author: kermit
'''
######################################
# FOC Forcaster - configuration file #
######################################

# True - all curves plotted on the same graph
# False - each curve plotted in a separate graph
combine_plots = True

# take data from start_date to end_date
start_date = 1980
end_date = 2010

# see codes at http://en.wikipedia.org/wiki/ISO_3166-1_alpha-3
__countries = """
usa
"""
# good data: can, usa

# see codes by selecting the desired indicators at http://databank.worldbank.org/
# , downloading the meta-file in excel format
# and copying the codes from the excel table
__indicators = """
SP.URB.TOTL.IN.ZS-Urban population (% of total)
SP.DYN.LE00.MA.IN-Life expectancy at birth, male (years)
"""
# population - SP.POP.TOTL
# real interest rate - FR.INR.RINR
# GDP per capita - NY.GDP.PCAP.KD
# unemployment rate - SL.UEM.TOTL.ZS
# GDP growth (annual %) - NY.GDP.MKTP.KD.ZG

__process_indicators = """
"""

# Visualisation options
#############################

# True - graphs written to files
# False - interactive graphs will be shown in a GUI
write_to_file = True

filename = "viz4.svg"

graph_title = "Urban population & male life expectancy\n5 years before and after observed crises/non-crises" 

label_dist_factor = 0.4

legend_loc = "lower right"
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


# Performance
##############

# pause in seconds between subsequent World Bank API queries
wb_pause = 0


########################################################
### INTERNAL STUFF - do not touch or be intimidated by:
########################################################
import re
#pattern = " |\n"
pattern = "\s"
newline = re.compile("[\n\r]")
whitespace = re.compile("\s|\b")
listify = lambda txt : [el.rstrip() for el in re.split(pattern,txt) if el!=""]
listify_newline = lambda txt : [el.rstrip() for el in newline.split(txt) if el!=""]
listify_no_tails = lambda txt : [el.split("-")[0].rstrip() for el in listify_newline(txt)]
listify_only_tails = lambda txt : [el.split("-", 1)[1].rstrip() for el in listify_newline(txt)]

countries = listify(__countries)
indicators = listify_no_tails(__indicators)
indicators_full = listify_newline(__indicators)
indicator_title_texts = listify_only_tails(__indicators)
indicator_titles = dict([(indicators[i], indicator_title_texts[i]) for i in range(len(indicators))])
process_indicators = set(listify(__process_indicators))
groups = [listify(x) for x in __events.split("*")]
colors = listify(__colors)
legend = listify(__legend)
