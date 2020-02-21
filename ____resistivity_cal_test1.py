# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 16:50:54 2020

@author: YWu
"""
import pandas as pd
from pathlib import Path

class Resistivity_Cal:
    
    def __init__(self, filepath_thk, filename_thk, filepath_Rs, filename_Rs):
        self.df_thk = self._read_df(filepath_thk, filename_thk)
        self.df_Rs = self._read_df(filepath_Rs, filename_Rs)
        thk_header = self._input_thk_col()
        if not thk_header:
            print('Wrong thickness column!')
            return
        Rs_header = self._input_Rs_col()
        if not Rs_header:
            print('Wrong Rs column!')
            return
        df = self._calculate_resistivity(thk_header, Rs_header)
        print('\n\n\n\n*********************************Please input the file path you want to save the resistivity data.\n For example, C:\\Users\\rawdata\\ \n (note: please use \\ instead of /, do not miss the last \\)\n You can skip by pressing enter. File will be saved under thickness data foler.\n\n*********************************')
        savepath = input()
        if not savepath:
            savepath = filepath_thk + 'ResistivityJMP/'
            savefilename = filename_thk[:-4] + 'Res_JMP.csv'
            self._save(df, savepath , savefilename)
            print('*********************************\nResistivity saved!\n*********************************')
            return
        print('\nPlease input the filename you want to save\n*********************************')
        savefilename = input() + '.csv'
        self._save(df, savepath , savefilename)
        print('*********************************\nResistivity saved!\n*********************************')
        return
        
    def _read_df(self, filepath, filename):
        df = pd.read_table(filepath + filename, 
                 index_col=False, sep=',',engine = 'python',error_bad_lines=False,warn_bad_lines=False,  keep_default_na=True,escapechar='\\')
        return df
    
    
    def _input_thk_col(self):
        print('Please select the thickness data column number or name.\n num: name.')
        d = dict()
        header = self.df_thk.columns.values.tolist()
        for i, h in enumerate(header):
            d[i] = h
            print('{} : '.format(i) + h)
        thk_col = input()
        if thk_col.isdigit():
            return d[int(thk_col)]
        else:
            return thk_col if thk_col in header else None
        
    def _input_Rs_col(self):
        print('Please select the Rs data column number or name.\n num: name.')
        d = dict()
        header = self.df_Rs.columns.values.tolist()
        for i, h in enumerate(header):
            d[i] = h
            print('{} : '.format(i) + h)
        Rs_col = input()
        if Rs_col.isdigit():
            return d[int(Rs_col)]
        else:
            return Rs_col if Rs_col in header else None
        
    
    
    def _calculate_resistivity(self, thk_header, Rs_header): #calculate res and return new df
        pts = 0
        first, second = 0, 0
        for i in range(len(self.df_thk)):
            if self.df_thk.loc[i]['X'] == 0 and self.df_thk.loc[i]['Y'] == 0:
                if not first:
                    first = i
                else:
                    second = i
                    break
        if not second:
            second = len(self.df_thk)
        pts = second - first
        num_of_wf_Rs = len(self.df_Rs)/pts
        num_of_wf_thk = len(self.df_thk)/pts
        linestoskip_Rs = 0
        linestoskip_thk = 0
        if not pts or num_of_wf_Rs != num_of_wf_thk:
            print('There are {} wafers in Rs file and {} wafers in thickness file.'.format(num_of_wf_Rs,num_of_wf_thk))
            print('\nPlease input the number of wafer as the first wafer to calculate resistivity for the file with more wafers.')
            wfstoskip = int(input()) - 1
            if num_of_wf_Rs> num_of_wf_thk:
                linestoskip_Rs = wfstoskip*pts
            else:
                linestoskip_thk = wfstoskip*pts
        df = pd.DataFrame()
        length = min(len(self.df_Rs), len(self.df_thk))
        for i in range(0, length, pts):
            df_thk1 = self.df_thk[i+linestoskip_thk:i+linestoskip_thk+pts]
            df_rs1 = self.df_Rs[i+linestoskip_Rs:i+linestoskip_Rs+pts]
            df_thk1['X'] = df_thk1['X'].round(decimals=1)
            df_thk1['Y'] = df_thk1['Y'].round(decimals=1)
            df_rs1['X'] = df_rs1['X'].round(decimals=1)
            df_rs1['Y'] = df_rs1['Y'].round(decimals=1)
            df_merge1 = pd.merge(df_rs1, df_thk1, on = ['X','Y'], how='inner')
            df_merge1['Resistivity'] = df_merge1[Rs_header]*df_merge1[thk_header]/100
            df = df.append(df_merge1)
        return df
    
    def _save(self, df, savepath , savefilename):
        output_dir = Path(savepath)
        output_dir.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_dir / savefilename)
        


################################TEST
if __name__ == '__main__':
    filepath_thk = 'C:/Users/ywu156243/Documents/Yong Wu/rawDATA/SPC930/JMP/'
    filename_thk = '1005188-417480_F3354_092219_Post_JQ_ALO03_s7-25_XRFJMP.csv'
    filepath_Rs = 'C:/Users/ywu156243/Documents/Yong Wu/rawDATA/SPC213/JMP/'
    filename_Rs = '1005114-JQ_ALO03_s7-25_RsJMP1.csv'
    Resistivity_Cal(filepath_thk, filename_thk, filepath_Rs, filename_Rs)
    
    
    
    
    
    
    
    
    
