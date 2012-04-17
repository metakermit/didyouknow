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

# take data from start_date to end_date
start_date = 1965
end_date = 2009

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
idn
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
TM.VAL.AGRI.ZS.UN-agr_imp
NV.AGR.TOTL.ZS-agr_val
SP.RUR.TOTL.ZS-rur_pop
SH.DYN.MORT-mort
SI.DST.FRST.20-income_low
SL.EMP.VULN.ZS-empl_bad
SE.XPD.PRIM.PC.ZS-ed_prim_ex
SE.XPD.TERT.PC.ZS-ed_tert_ex
SE.ADT.1524.LT.ZS-lit_youth
SE.XPD.TOTL.GD.ZS-edu_spend
EG.IMP.CONS.ZS-en_import
AG.LND.FRST.ZS-forest
NY.ADJ.DKAP.GN.ZS-adj_sav
NY.GDP.TOTL.RT.ZS-nat_res_re
FB.BNK.CAPA.ZS-catp_to_as
FS.LBL.LIQU.GD.ZS-m3
CM.MKT.LCAP.GD.ZS-comp_capit
FM.LBL.MQMY.ZG-mon_growth
FM.LBL.MQMY.GD.ZS-m2
IC.CRD.PRVT.ZS-cred_cover
FS.LBL.QLIQ.GD.ZS-quasi
CM.MKT.TRNR-stocks
BX.TRF.PWKR.DT.GD.ZS-worker_rem
SL.TLF.PART.MA.ZS-emp_part_m
SL.TLF.PART.FE.ZS-emp_part_f
SL.UEM.LTRM.MA.ZS-unemp_m
SL.UEM.LTRM.FE.ZS-unemp_f
SE.ADT.1524.LT.FM.ZS-lit_f
SE.PRM.NENR.FE-edu_prim_f
SE.PRM.NENR.MA-edu_prim_m
SE.SEC.NENR.FE-edu_sec_f
SE.SEC.NENR.MA-edu_sec_m
SE.TER.ENRR.FE-edu_tert_f
SE.TER.ENRR.MA-edu_tert_m
SP.DYN.TO65.FE.ZS-surv_65_f
SP.DYN.TO65.MA.ZS-surv_65_m
SL.TLF.CACT.FE.ZS-labor_f
SL.TLF.CACT.MA.ZS-labor_m
SL.TLF.CACT.ZS-labor_part
SP.DYN.LE00.FE.IN-life_exp_f
SP.DYN.LE00.MA.IN-life_exp_m
SH.MMR.RISK.ZS-matern_dea
SE.PRM.TENR.FE-edu_total_
SE.PRM.TENR.MA-edu_total_2
SL.UEM.TOTL.FE.ZS-unem_f
SL.UEM.TOTL.MA.ZS-unem_m
SL.UEM.PRIM.FE.ZS-unem_prim_
SL.UEM.PRIM.MA.ZS-unem_prim_2
SL.UEM.SECO.FE.ZS-unem_sec_f
SL.UEM.SECO.MA.ZS-unem_sec_m
SL.UEM.TERT.FE.ZS-unem_tert_
SH.XPD.TOTL.ZS-health_pub
SP.POP.0014.TO.ZS-pop_14
SP.POP.1564.TO.ZS-pop_15_64
SP.POP.65UP.TO.ZS-pop_64
SP.POP.TOTL.FE.ZS-pop_f
SP.POP.GROW-pop_growth
TM.VAL.ICTG.ZS.UN-import_ict
IS.ROD.ENGY.ZS-en_roads
SL.AGR.EMPL.FE.ZS-agr_f
SL.AGR.EMPL.MA.ZS-agr_m
SL.IND.EMPL.FE.ZS-empl_indus
SL.IND.EMPL.MA.ZS-empl_indus2
SL.SRV.EMPL.FE.ZS-empl_serv_
SL.SRV.EMPL.MA.ZS-empl_serv_2
SL.AGR.EMPL.ZS-empl_agr
SL.EMP.TOTL.SP.ZS-empl_pop
SL.UEM.LTRM.ZS-unempl_lon
SL.UEM.1524.FE.ZS-unempl_you
SL.UEM.1524.MA.ZS-unempl_you2
SI.DST.04TH.20-income_4th
SI.DST.10TH.10-income_hig
SI.DST.05TH.20-income_hig2
SI.DST.FRST.10-income_low2
SI.DST.FRST.20-income_low3
SI.DST.02ND.20-income_2nd
SI.DST.03RD.20-income_3rd
SI.POV.NAGP-pov_gap_na
SI.POV.RUGP-pov_gap_ru
SI.POV.URGP-pov_gap_ur
SI.POV.DDAY-pov_count_
SI.POV.2DAY-pov_count_2
SI.POV.NAHC-pov_count_3
SI.POV.RUHC-pov_count_4
SI.POV.URHC-pov_count_5
TX.VAL.TECH.MF.ZS-export_tec
GB.XPD.RSDV.GD.ZS-expense_r_
SL.TLF.0714.FE.ZS-eco_active
SL.TLF.0714.MA.ZS-eco_active2
SL.TLF.0714.SW.FE.ZS-eco_active3
SL.TLF.0714.SW.MA.ZS-eco_active4
SL.TLF.0714.ZS-eco_active5
SL.TLF.0714.WK.FE.ZS-eco_active6
SL.TLF.0714.WK.MA.ZS-eco_active7
EN.URB.LCTY.UR.ZS-pop_larges
EN.URB.MCTY.TL.ZS-pop_millio
IS.ROD.ENGY.ZS-en_road
SP.URB.TOTL.IN.ZS-urban_pop
BN.CAB.XOKA.GD.ZS-bal
GC.DOD.TOTL.GD.ZS-debt
FS.AST.PRVT.GD.ZS-cred
BX.KLT.DINV.WD.GD.ZS-FDI
FB.BNK.CAPA.ZS-bnk_hlth
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
sample_selection_file = "crises-imf-banking.xls"
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

# if this is True, only the neccessary data will be downloaded
# in multiple queries (but it takes longer),
# if this is False, the program downloads all the values between
# start and end years in one query (per indicator per country),
# which is faster (or so it seems)
sparse = False


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
