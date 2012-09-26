'''
Created on 14. 12. 2011.

@author: kermit
'''
######################################
# FOC Forcaster - configuration file #
######################################

# Data semantics
################

# location where to save the data
# (don't specify the extension, as that is determined by the formatter)
output_location = "io/data_105_2012_delta_banking+currency+debt"

# take data from start_date to end_date
start_date = 1950
end_date = 2015

# see codes at http://en.wikipedia.org/wiki/ISO_3166-1_alpha-3
# a special value of EVERYTHING (as a first country) takes everything that has a crisis or normal year
# defined in the sample definition XLS file intersected with the countries offered
# by the World Bank
__countries = """
EVERYTHING
"""
# good data: can, usa

# indicators to analyse as potential features that caused the crises
# see codes by selecting the desired indicators at http://databank.worldbank.org/
# and copying the codes from the ending of the url
__indicators = """
SL.AGR.EMPL.ZS-agr_emp-Employment in agriculture (% of total employment)
TX.VAL.AGRI.ZS.UN-agr_exp-Agricultural raw materials exports (% of merchandise exports) 
TM.VAL.AGRI.ZS.UN-agr_imp-Agricultural raw materials imports (% of merchandise imports) 
NV.AGR.TOTL.ZS-agr_val-Agriculture, value added (% of GDP)
SP.RUR.TOTL.ZS-rur_pop-Rural population (% of total population)
SH.DYN.MORT-mort-Mortality rate, under-5 (per 1,000) 
SI.DST.FRST.20-income_lowest-Income share held by lowest 20% 
SL.EMP.VULN.ZS-empl_bad-Vulnerable employment, total (% of total employment) 
SE.XPD.PRIM.PC.ZS-ed_prim_exp-Expenditure per student, primary (% of GDP per capita)
SE.XPD.TERT.PC.ZS-ed_tert_exp-Expenditure per student, tertiary (% of GDP per capita) 
SE.ADT.1524.LT.ZS-lit_youth-Literacy rate, youth total (% of people ages 15-24)
SE.XPD.TOTL.GD.ZS-edu_spend-Public spending on education, total (% of GDP)
EG.IMP.CONS.ZS-en_import-Energy imports, net (% of energy use)
AG.LND.FRST.ZS-forest-Forest area (% of land area) 
NY.ADJ.DKAP.GN.ZS-adj_sav-Adjusted savings: consumption of fixed capital (% of GNI)
NY.GDP.TOTL.RT.ZS-nat_res_rent-Total natural resources rents (% of GDP)
FB.BNK.CAPA.ZS-catp_to_asset-Bank capital to assets ratio (%)
FS.LBL.LIQU.GD.ZS-m3-Liquid liabilities (M3) as % of GDP
CM.MKT.LCAP.GD.ZS-comp_capit-Market capitalization of listed companies (% of GDP)
FM.LBL.MQMY.ZG-mon_growth-Money and quasi money growth (annual %)
FM.LBL.MQMY.GD.ZS-m2-Money and quasi money (M2) as % of GDP
IC.CRD.PRVT.ZS-cred_cover-Private credit bureau coverage (% of adults)
FS.LBL.QLIQ.GD.ZS-quasi-Quasi-liquid liabilities (% of GDP)
CM.MKT.TRNR-stocks-Stocks traded, turnover ratio (%)
BX.TRF.PWKR.DT.GD.ZS-worker_remit-Workers' remittances and compensation of employees, received (% of GDP)
SL.TLF.PART.MA.ZS-emp_part_m-Part time employment, male (% of total male employment)
SL.TLF.PART.FE.ZS-emp_part_f-Part time employment, female (% of total female employment)
SL.UEM.LTRM.MA.ZS-unemp_m-Long-term unemployment, male (% of male unemployment)
SL.UEM.LTRM.FE.ZS-unemp_f-Long-term unemployment, female (% of female unemployment)
SE.ADT.1524.LT.FM.ZS-lit_f-Ratio of young literate females to males (% ages 15-24) 
SE.PRM.NENR.FE-edu_prim_f-School enrollment, primary, female (% net)
SE.PRM.NENR.MA-edu_prim_m-School enrollment, primary, male (% net)
SE.SEC.NENR.FE-edu_sec_f-School enrollment, secondary, female (% net)
SE.SEC.NENR.MA-edu_sec_m-School enrollment, secondary, male (% net)
SE.TER.ENRR.FE-edu_tert_f-School enrollment, tertiary, female (% gross)
SE.TER.ENRR.MA-edu_tert_m-School enrollment, tertiary, male (% gross)
SP.DYN.TO65.FE.ZS-surv_65_f-Survival to age 65, female (% of cohort)
SP.DYN.TO65.MA.ZS-surv_65_m-Survival to age 65, male (% of cohort)
SL.TLF.CACT.FE.ZS-labor_f-Labor participation rate, female (% of female population ages 15+)
SL.TLF.CACT.MA.ZS-labor_m-Labor participation rate, male (% of male population ages 15+)
SL.TLF.CACT.ZS-labor_particip_rate-Labor participation rate, total (% of total population ages 15+)
SP.DYN.LE00.FE.IN-life_exp_f-Life expectancy at birth, female (years)
SP.DYN.LE00.MA.IN-life_exp_m-Life expectancy at birth, male (years)
SH.MMR.RISK.ZS-matern_death-Lifetime risk of maternal death (%)
SE.PRM.TENR.FE-edu_total_f-Total enrollment, primary, female (% net)
SE.PRM.TENR.MA-edu_total_m-Total enrollment, primary, male (% net)
SL.UEM.TOTL.FE.ZS-unem_f-Unemployment, female (% of female labor force)
SL.UEM.TOTL.MA.ZS-unem_m-Unemployment, male (% of male labor force)
SL.UEM.PRIM.FE.ZS-unem_prim_f-Unemployment with primary education, female (% of female unemployment)
SL.UEM.PRIM.MA.ZS-unem_prim_m-Unemployment with primary education, male (% of male unemployment)
SL.UEM.SECO.FE.ZS-unem_sec_f-Unemployment with secondary education, female (% of female unemployment)
SL.UEM.SECO.MA.ZS-unem_sec_m-Unemployment with secondary education, male (% of male unemployment)
SL.UEM.TERT.FE.ZS-unem_tert_f-Unemployment with tertiary education, female (% of female unemployment)
SH.XPD.TOTL.ZS-health_pub-Health expenditure, public (% of GDP)
SP.POP.0014.TO.ZS-pop_14-Population ages 0-14 (% of total)
SP.POP.1564.TO.ZS-pop_15_64-Population ages 15-64 (% of total)
SP.POP.65UP.TO.ZS-pop_64-Population ages 65 and above (% of total)
SP.POP.TOTL.FE.ZS-pop_f-Population, female (% of total)
SP.POP.GROW-pop_growth-Population growth (annual %)
TM.VAL.ICTG.ZS.UN-import_ict-ICT goods imports (% total goods imports)
IS.ROD.ENGY.ZS-en_roads-Road sector energy consumption (% of total energy consumption)
SL.AGR.EMPL.FE.ZS-agr_f-Employees, agriculture, female (% of female employment)
SL.AGR.EMPL.MA.ZS-agr_m-Employees, agriculture, male (% of male employment)
SL.IND.EMPL.FE.ZS-empl_indust_f-Employees, industry, female (% of female employment)
SL.IND.EMPL.MA.ZS-empl_indust_m-Employees, industry, male (% of male employment)
SL.SRV.EMPL.FE.ZS-empl_serv_f-Employees, services, female (% of female employment)
SL.SRV.EMPL.MA.ZS-empl_serv_m-Employees, services, male (% of male employment)
SL.AGR.EMPL.ZS-empl_agr-Employment in agriculture (% of total employment)
SL.EMP.TOTL.SP.ZS-empl_pop-Employment to population ratio, 15+, total (%)
SL.UEM.LTRM.ZS-unempl_long-Long-term unemployment (% of total unemployment)
SL.UEM.1524.FE.ZS-unempl_youth_f-Unemployment, youth female (% of female labor force ages 15-24)
SL.UEM.1524.MA.ZS-unempl_youth_m-Unemployment, youth male (% of male labor force ages 15-24)
SI.DST.04TH.20-income_4th_20-Income share held by fourth 20%
SI.DST.10TH.10-income_high_10-Income share held by highest 10%
SI.DST.05TH.20-income_high_20-Income share held by highest 20%
SI.DST.FRST.10-income_low_10-Income share held by lowest 10%
SI.DST.FRST.20-income_low_20-Income share held by lowest 20%
SI.DST.02ND.20-income_2nd_20-Income share held by second 20%
SI.DST.03RD.20-income_3rd_20-Income share held by third 20%
SI.POV.NAGP-pov_gap_national-Poverty gap at national poverty line (%)
SI.POV.RUGP-pov_gap_rural-Poverty gap at rural poverty line (%)
SI.POV.URGP-pov_gap_urban-Poverty gap at urban poverty line (%)
SI.POV.DDAY-pov_count_1_25-Poverty headcount ratio at $1.25 a day (PPP) (% of population)
SI.POV.2DAY-pov_count_2-Poverty headcount ratio at $2 a day (PPP) (% of population)
SI.POV.NAHC-pov_count_national-Poverty headcount ratio at national poverty line (% of population)
SI.POV.RUHC-pov_count_rural-Poverty headcount ratio at rural poverty line (% of rural population)
SI.POV.URHC-pov_count_urban-Poverty headcount ratio at urban poverty line (% of urban population)
TX.VAL.TECH.MF.ZS-export_tech-High-technology exports (% of manufactured exports)
GB.XPD.RSDV.GD.ZS-expense_r_d-Research and development expenditure (% of GDP)
SL.TLF.0714.FE.ZS-eco_active_child_f-Economically active children, female (% of female children ages 7-14)
SL.TLF.0714.MA.ZS-eco_active_child_m-Economically active children, male (% of male children ages 7-14)
SL.TLF.0714.SW.FE.ZS-eco_active_child_stud_work_f-Economically active children, study and work, female (% of female economically active children, ages 7-14)
SL.TLF.0714.SW.MA.ZS-eco_active_child_stud_work_m-Economically active children, study and work, male (% of male economically active children, ages 7-14)
SL.TLF.0714.ZS-eco_active_child-Economically active children, total (% of children ages 7-14)
SL.TLF.0714.WK.FE.ZS-eco_active_child_work_f-Economically active children, work only, female (% of female economically active children, ages 7-14)
SL.TLF.0714.WK.MA.ZS-eco_active-child_work_m-Economically active children, work only, male (% of male economically active children, ages 7-14)
EN.URB.LCTY.UR.ZS-pop_largest_city-Population in the largest city (% of urban population)
EN.URB.MCTY.TL.ZS-pop_million_city-Population in urban agglomerations of more than 1 million (% of total population)
IS.ROD.ENGY.ZS-en_road-Road sector energy consumption (% of total energy consumption)
SP.URB.TOTL.IN.ZS-urban_pop-Urban population (% of total)
BN.CAB.XOKA.GD.ZS-bal-current account balance (sum of net exports, net income, and net current transfers
GC.DOD.TOTL.GD.ZS-debt-central government debt
FS.AST.PRVT.GD.ZS-cred-domestic credit to private sector (excessive booms important)
BX.KLT.DINV.WD.GD.ZS-FDI-foreign direct inflows (capital inflows)
FB.BNK.CAPA.ZS-bnk_hlth-bank capital to assets ratio (bank's health)
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
sample_selection_file = "io/imf/2012_delta/crisis-imf-2012-delta-banking+currency+debt.xls"
#sample_selection_file = "../odabir_uzoraka-rucni-mali.xls"

# how many years to look back searching for crises causes
look_back_years = 3

# what percentage of the dataset to use _only_ for testing
testing_percentage = 0.0

# output formats available: TSV or SGD
output_formats = ["SGD","TSV"]

# Performance
##########

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

listify = lambda txt : [el.upper() for el in txt.split("\n") if el!=""]
listify_no_tails = lambda txt : [el.split("-")[0].upper() for el in txt.split("\n") if el!=""]

countries = listify(__countries)
indicators_with_translations = listify(__indicators)
indicators = listify_no_tails(__indicators)
process_indicators = set(listify(__process_indicators))
state_indicators = listify(__state_indicators)
