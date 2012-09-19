'''
Created on 14. 12. 2011.

@author: kermit
'''
######################################
# FOC Forcaster - configuration file #
######################################

# Graphs
########

# True - graphs written to files
# False - interactive graphs will be shown in a GUI
write_to_file = True

# True - all curves plotted on the same graph
# False - each curve plotted in a separate graph
combine_plots = True

# Data semantics
################

# location where to save the data
# (don't specify the extension, as that is determined by the formatter)
output_location = "io/dataset"

# take data from start_date to end_date
start_date = 1965
end_date = 2009

# see codes at http://en.wikipedia.org/wiki/ISO_3166-1_alpha-3
__countries = """
nor
usa
bra
"""
# good data: can, usa

# indicators to analyse as potential features that caused the crises
# see codes by selecting the desired indicators at http://databank.worldbank.org/
# and copying the codes from the ending of the url
__indicators = """
SL.AGR.EMPL.ZS-agr_emp
FS.AST.PRVT.GD.ZS-cred
BX.KLT.DINV.WD.GD.ZS-FDI
"""

# some indicators include:
# population - SP.POP.TOTL
# real interest rate - FR.INR.RINR
# GDP per capita - NY.GDP.PCAP.KD
# unemployment rate - SL.UEM.TOTL.ZS-unempl
# GDP growth (annual %) - NY.GDP.MKTP.KD.ZG-gdp
# population 65+ - SP.POP.65UP.TO.ZS-pop65
#
# These are possible crisis causes according to IMF's "Systemic Banking Crises: A New Database":
# current account balance (sum of net exports, net income, and net current transfers) - BN.CAB.XOKA.GD.ZS-bal
# central government debt - GC.DOD.TOTL.GD.ZS-debt
# domestic credit to private sector (excessive booms important) - FS.AST.PRVT.GD.ZS-cred
# foreign direct inflows (capital inflows) - BX.KLT.DINV.WD.GD.ZS-FDI
# bank capital to assets ratio (bank's health) - FB.BNK.CAPA.ZS-bnk_hlth


# the indicators which are to be processed among the ones above (if they exist above)
# processing currently means:
# - calculating a derivative over all the values
__process_indicators = """
FR.INR.RINR
SL.UEM.TOTL.ZS
"""
# makes sense to process:
# FR.INR.RINR
# SL.UEM.TOTL.ZS

# AI
#######

# indicators to use as  state (crysis/normal) determinators
# NOT IMPLEMENTED YET
__state_indicators = """
SP.POP.65UP.TO.ZS
"""

# choose the dates when crises happened in this file
sample_selection_file = "io/crises-imf-banking.xls"
#sample_selection_file = "../odabir_uzoraka-rucni-mali.xls"

# how many years to look back searching for crises causes
look_back_years = 3

# what percentage of the dataset to use _only_ for testing
testing_percentage = 0.0

# output format: TSV or SGD
output_format = "TSV"

# Performance
##########

# pause in seconds between subsequent World Bank API queries
wb_pause = 0


########################################################
### INTERNAL STUFF - do not touch or be intimidated by:
########################################################

listify = lambda txt : [el.upper() for el in txt.split("\n") if el!=""]
listify_no_tails = lambda txt : [el.split("-")[0].upper() for el in txt.split("\n") if el!=""]

countries = listify(__countries)
indicators_with_translations = listify(__indicators)
indicators = listify_no_tails(__indicators)
process_indicators = set(listify(__process_indicators))
state_indicators = listify(__state_indicators)
