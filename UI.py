# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 10:50:44 2020

@author: ywu
"""
from format import Format
from read_excel_data import Read_Excel
from resistivity_cal import Resistivity_Cal

class UI:
    def __init__(self):
        self.FORMAT = Format()
        self.format_dict = self.FORMAT.read_format_dict() # format dict
        self.interface()
    
    def interface(self):
        self.welcome()
        userinput = input()
        while not userinput.isdigit() and userinput != 'exit':
            print('invalid input, please enter a number')
            userinput = input()
        if userinput == '1':
            self.interface_fun1() #Convert the raw excel data from metrology to JMP readable point to point data file
        elif userinput == '2':
            self.interface_fun2() #Calculate the resistivity based on thk and Rs. And convert the result to point to point JMP file.
        elif userinput == '3':
            self.interface_fun3() #Check the existing format.
        elif userinput == '4':
            self.interface_fun4() #Delete the existing format.
        elif userinput == 'exit':
            return
        
    
    def welcome(self):
        print('Welcome to use JMP format script. \nHere are the functions we have:\n 1. Convert the raw excel data from metrology to JMP readable point to point data file. \n 2. Calculate the resistivity based on thk and Rs. And convert the result to point to point JMP file. \n 3. Check the existing format. \n 4. Delete the existing format.  \n\n  Please type the number of functions you want to use. Type exit to quit script.')
        
    def interface_fun1(self):
        print('Please input the tool number')
        tool = str(input())
        print('Please input the film type (eg. W, TiN, or code name...)')
        film = input()
        film = str(film).lower()
        key = (tool, film)
        if key in self.format_dict:
            pts, cols, rows = self.format_dict[key]
            print('Please input the file path. For example, C:\\Users\\rawdata\\ \n (note: please use \\ instead of /, do not miss the last \\) ')
            filepath = input()
            filepath = self.cleanfilepath(filepath)
            print('Please input the csv file name. For example, F2968_Post_ALO12_s1-10_XRF_930.csv')
            filename = input()
            filename = self.cleanfilename(filename)
            EXCEL = Read_Excel(filepath,filename)
#            df = EXCEL.export_dataframe() # for test
            EXCEL.Auto_Save(pts = pts, cols = cols, rows = rows)
            print('*************************\n Done. Auto saved to same path JMP folder. \n*************************')
            
        else:
            print('*************************\n *************************\n Can not find the existing format, please follow the instructions. \n ')
#            tool = input()
#            print('Please input the film type (eg. W, TiN, or any code name)')
#            film = input()
#            film = str(film).lower()
            print('Please input the number of points you measure in this wafer (eg. 49, 625)')
            pts = int(input())
            print('Please input the ID of the columns you want to keep, usually you want to keep X, Y coordinates, slot ID and data you are interested. \n Input like, C D F ')
            cols = self.helper_cols_input(input())
            print('Please input the first row number and second row number where you have numeric value you want to keep. \n input eg. 14 16 \n You can skip this step by pressing Enter. Software will try to auto detect.')
            rows = self.helper_rows_input(input())
            print('Please input the file path. For example, C:\\Users\\rawdata\\ \n (note: please use \\ instead of /, do not miss the last \\) ')
            filepath = input()
            filepath = self.cleanfilepath(filepath)
            print('Please input the csv file name. For example, F2968_Post_ALO12_s1-10_XRF_930.csv')
            filename = input()
            filename = self.cleanfilename(filename)
            EXCEL = Read_Excel(filepath,filename)
            rowschecked = EXCEL.auto_check_format()
            if rowschecked != rows:
                rows = rowschecked
            EXCEL.Auto_Save(pts = pts, cols = cols, rows = rows)
            print('*************************\n Done. Auto saved to same path JMP folder. \n*************************')
            self.FORMAT.create_new_format(tool, film, pts, cols, rows)
            print('*************************\n New format created. Next time, you can retrieve this format by input tool: ' + tool + ' and film: ' + film + '\n*************************')
        return [filepath, filename]
            
        
    def interface_fun2(self): # cal the resistivity point to point. Use the nearest neighbor to pair the X, Y coordinates
        print('Do you already have JMP readable file? If Yes, press 1. Else, press 2.')
        fun = input()
        if fun == '1':
            self.interface_fun2_1() # combine two JMP readable file
        elif fun == '2':
            self.interface_fun2_2() # Start from scratch, one Thk Raw Data, One Rs raw data.
        else:
            print('Wrong input!')
            return
        
    def interface_fun2_1(self):
        print('Please input the thickness data file path.\n For example, C:\\Users\\rawdata\\ \n (note: please use \\ instead of /, do not miss the last \\) ')
        filepath_thk = input()
        filepath_thk = self.cleanfilepath(filepath_thk)
        print('Please input the thickness data file name.')
        filename_thk = self.cleanfilename(input())
        print('Please input the Rs data file path.\n For example, C:\\Users\\rawdata\\ \n (note: please use \\ instead of /, do not miss the last \\) ')
        filepath_Rs = input()
        filepath_Rs = self.cleanfilepath(filepath_Rs)
        print('Please input the Rs data file name.')
        filename_Rs = self.cleanfilename(input())
        self.resistivity_cal(filepath_thk, filename_thk, filepath_Rs, filename_Rs)
    
    def interface_fun2_2(self):
        print('\n\nPlease input the thickness raw data information\n')
        filepath_thk, filename_thk = self.interface_fun1()
        filepath_thk += 'JMP' + chr(92)
        filename_thk = filename_thk[:-4] + 'JMP.csv'
        print('\n\nPlease input the Rs raw data information\n')
        filepath_Rs, filename_Rs = self.interface_fun1()
        filepath_Rs += 'JMP' + chr(92)
        filename_Rs = filename_Rs[:-4] + 'JMP.csv'
        self.resistivity_cal(filepath_thk, filename_thk, filepath_Rs, filename_Rs)
        
        
    def resistivity_cal(self, filepath_thk, filename_thk, filepath_Rs, filename_Rs):
        Resistivity_Cal(filepath_thk, filename_thk, filepath_Rs, filename_Rs)
    
    
    def interface_fun3(self):
        print('********************************')
        for key in sorted(self.format_dict.keys()):
            print('tool: ' + key[0] + '  film: ' + key[1] + '\n')
            pts, cols, rows = self.format_dict[key]
            print('number of points: {}'.format(pts)  + '   cols used in raw excel: {}'.format(cols) + '   first row and step (between two wafer): {}'.format(rows) )
            print('\n \n')
        print('********************************')
        #self.interface() # return to main page
        
    def interface_fun4(self):
        print('Please input the existing format\'s tool number you want to delete: ')
        tool = str(input())
        print('Please input the existing format\'s film name you want to delete: ')
        film = input()
        film = str(film).lower()
        key = (tool, film)
        if key not in self.format_dict:
            print('Not Found\n')
            return
        self.FORMAT.del_format(tool,film)
        print('Deleted!!!')
        
    
    def cleanfilepath(self, filepath):
        if filepath[-1]!=chr(92):
            filepath += chr(92)
        #filepath = filepath.replace(' ', '')
        return filepath
    
    def cleanfilename(self,filename):
        if filename[-4:] != '.csv':
            filename = filename + '.csv'
        return filename
    
    def helper_cols_input(self,s):
        d = {}
        for i in range(26):
            key = ord('A') + i
            d[chr(key)] = i
        s = s.split(' ')
        cols= []
        for char in s:
            cols.append(d[char.upper()])
        return cols
        
    def helper_rows_input(self,s):
        if not s:
            return None
        s= s.split(' ')
        if len(s) == 1:
            return [int(s[0])-2, None]
        return [int(s[0])-2, int(s[1])-int(s[0])]
        
        
    