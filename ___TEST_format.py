# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 16:16:43 2020

@author: YWu
"""

from format import Format
            
if __name__ == '__main__':
    pts = 49
    cols = [0,5,6,8]
    rows = [12,55]
    tool = 'TESTTESTTESTTESTTEST'
    film = 'TESTTESTTESTTEST'
    FORMAT = Format()
    FORMAT.create_new_format(tool, film, pts, cols, rows)
    FORMAT.del_format(tool, film)
    d = FORMAT.read_format_dict()
    print(d)