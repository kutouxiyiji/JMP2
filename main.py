# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 13:13:56 2020

@author: YWu

readme_1:
    1. format is (tool, film) : [number of points, interested cols, [first row, step]]
    2. Please use a different film name for 625pts. For example, w625
    3. 
"""

from format import Format
from read_excel_data import Read_Excel
from UI import UI
            
if __name__ == '__main__':
    run = UI()