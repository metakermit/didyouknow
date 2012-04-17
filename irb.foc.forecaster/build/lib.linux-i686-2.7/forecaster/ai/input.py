'''
Created on 16. 12. 2011.

@author: kermit
'''
import xlrd

class Input(object):
    '''
    parser for input data
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def parse_sample_selection_to_list(self, location):
        crises_dates = []
        normal_dates = []
        wb = xlrd.open_workbook(location)
        # print(wb.sheet_names())
        sh = wb.sheet_by_index(0)
        for rownum in range(sh.nrows):
            values = [int(x) for x in sh.row_values(rownum)[2:] if x!=""]
            if rownum % 2 == 0:
                crises_dates.extend(values)
            else:
                normal_dates.extend(values)
            #print(sh.row_values(rownum))
        return (crises_dates, normal_dates)
    
    def parse_sample_selection(self, location):
        crises_dates = {}
        normal_dates = {}
        wb = xlrd.open_workbook(location)
        # print(wb.sheet_names())
        sh = wb.sheet_by_index(0)
        for rownum in range(sh.nrows):
            values = [int(x) for x in sh.row_values(rownum)[2:] if x!=""]
            if rownum % 2 == 0:
                country = sh.cell(rownum, 0).value
                crises_dates[country] =  values
            else:
                normal_dates[country] = values
            #print(sh.row_values(rownum))
        return (crises_dates, normal_dates)
            
            
            
            
            
            
            
            
            
            
            