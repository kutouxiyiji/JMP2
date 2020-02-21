# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 13:15:00 2020

@author: YWu
"""
import pandas as pd
from pathlib import Path

class Read_Excel:

    def __init__(self, path, filename, skiprows = 0):
        my_cols = [chr(97+i) for i in range(26)]
        self.path = path
        self.filename = filename
        self.skiprows = skiprows
        self.df = pd.read_table(path + filename,header=None, 
                 index_col=False,names=my_cols, skiprows=skiprows,sep=',',engine = 'python',error_bad_lines=False,warn_bad_lines=False,  keep_default_na=True,escapechar='\\')
    
    
    def export_dataframe(self):
        return self.df
    
    def read_cell(self,row,col):
        df = self.df
        val = df.iloc[row,col]
        if val:
            return val
        if not val:
            return False
    
    def read_range(self,cols,row1,row2): #including row1 not including row2
        if type(cols) == int:
            cols = [cols]
        df = self.df
        df2 = pd.DataFrame()
        df2 = df2.append(df.iloc[row1:row2,cols], ignore_index=True)
        return df2
    
    def auto_check_format(self, keywords = None):
        if not keywords:
            keywords = ['X','Y']
        df = self.df
        res = [None,None] # first row of data and step
        for i in range(len(df)):
            row = df.iloc[i,]
            temp = []
            for keyword in keywords:
                temp.append(any(row.isin([keyword])))
            if all(temp) and not res[0]:
                res[0] = i + 1
            elif all(temp) and not res[1]:
                res[1] = i + 1 -res[0]
                return res
        return res
    
    def check_header_name(self, cols, rows = None):
        if not rows:
            rows = self.auto_check_format()
        if type(cols) == int:
            cols = [cols]
        headerrow = rows[0]-1
        header= []
        df = self.df
        for col in cols:
            header.append(df.iloc[headerrow, col])
        return header
    
    def clean_excel(self,pts, cols, rows = None): # cols is list [col#1, col#2....] rows is a list [firstrow, step] pts is 49 pts or 625 pts measurement
        if not rows:
            rows = self.auto_check_format()
        df3 = pd.DataFrame()
        firstrow, step = rows
        df = self.df
        if not step:
            step = len(df)
        for row in range(firstrow, len(df), step):
            df3 = df3.append(self.read_range(cols,row, row+pts), ignore_index=True)
        return df3
    
    def Auto_Save(self, pts, cols, rows = None, savepath = None, savefilename=None): # add keywords = None as parameter?
        if not rows:
            rows = self.auto_check_format()
        df3 = self.clean_excel(pts,cols,rows)
        header = self.check_header_name(cols,rows)
        df3 = pd.DataFrame(df3.values, columns = header)
        if not savepath:
            savepath = self.path + 'JMP/'
        if not savefilename:
            savefilename = self.filename[:-4] + 'JMP.csv'
        output_dir = Path(savepath)
        output_dir.mkdir(parents=True, exist_ok=True)
        df3.to_csv(output_dir / savefilename)
 
#####test part

#if __name__ == '__main__':
#    
#    path = 'C:/Users/ywu156243/Documents/Yong Wu/rawDATA/SPC930/'
#    filename = '1035835-437386_F2968_111319_Post_JQ_ALO12_s1-10_XRF_930.csv'
#    EXCEL = Read_Excel(path,filename)
#    df = EXCEL.export_dataframe()
#    cols = [0,5,6,8]
#    rows = [12,55]
#    pts = 49
##    #print(df.head())
##    val = EXCEL.read_cell(1,0)
##    #print(val)
##    datatest = EXCEL.read_range([0,5,6,8],12,60)
##    #print(datatest.head())
##    cleandata = EXCEL.clean_excel(49,[0,5,6,8],[12,55])
##    #print(cleandata)
##    header = EXCEL.check_header_name(cols,rows)
##    #print(header)
#    EXCEL.Auto_Save(pts = pts, cols = cols, rows = rows)


