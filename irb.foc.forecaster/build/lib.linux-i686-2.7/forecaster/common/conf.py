'''
Created on 14. 12. 2011.

@author: kermit
'''
######################################
# FOC Forcaster - configuration file #
######################################

# Graphs
######

# True - graphs written to files
# False - interactive graphs will be shown in a GUI
write_to_file = True

# True - all curves plotted on the same graph
# False - each curve plotted in a separate graph
combine_plots = True

# Data semantics
############

# take data from start_date to end_date
start_date = 1965
end_date = 2007

# see codes at http://en.wikipedia.org/wiki/ISO_3166-1_alpha-3
__countries = """
alb
dza
arg
arm
aze
bgd
blr
ben
bmu
bih
bra
bgr
bfa
bdi
cmr
cpv
caf
tcd
chl
chn
col
cod
cog
cri
civ
hrv
cze
dji
dom
ecu
egy
slv
gnq
eri
est
fin
geo
gha
gin
gnb
guy
hti
hun
ind
isr
jam
jpn
jor
ken
kor
kwt
kgz
lva
lbn
lbr
ltu
mkd
mdg
mys
mli
mrt
mex
mar
moz
npl
nic
ner
nga
nor
pan
pry
per
phl
pol
rou
rus
stp
sen
sle
svk
svn
esp
lka
swz
swe
tza
tha
tgo
tun
tur
uga
ukr
gbr
usa
ury
yem
zmb
zwe
"""
# good data: can, usa

# indicators to analyse as potential features that caused the crises
# see codes by selecting the desired indicators at http://databank.worldbank.org/
# and copying the codes from the ending of the url
__indicators = """
SL.AGR.EMPL.ZS-agr_emp
TX.VAL.AGRI.ZS.UN-agr_exp
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
sample_selection_file = "odabir_uzoraka-imf-odabrane.xls"
#sample_selection_file = "../odabir_uzoraka-rucni-mali.xls"

# how many years to look back searching for crises causes
look_back_years = 3

# what percentage of the dataset to use _only_ for testing
testing_percentage = 0.0

# Performance
##########

# pause in seconds between subsequent World Bank API queries
wb_pause = 0

# if this is True, only the neccessary data will be downloaded
# in multiple queries (but it takes longer),
# if this is False, the program downloads all the values between
# start and end years in one query (per indicator per country),
# which is faster (or so it seems)
sparse = False


########################################################
### INTERNAL STUFF - do not touch or be intimidated by:
########################################################

listify = lambda txt : [el for el in txt.split("\n") if el!=""]
listify_no_tails = lambda txt : [el.split("-")[0] for el in txt.split("\n") if el!=""]

countries = listify(__countries)
indicators_with_translations = listify(__indicators)
indicators = listify_no_tails(__indicators)
process_indicators = set(listify(__process_indicators))
state_indicators = listify(__state_indicators)
