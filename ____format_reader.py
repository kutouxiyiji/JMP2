# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 16:50:54 2020

@author: YWu
"""

from format import Format

if __name__ == '__main__':
    pts = 49
    cols = [0,5,6,8]
    rows = [12,55]
    tool = '930'
    film = 'w'
    fmt = Format()
    fmt.create_format(tool, film, pts, cols, rows)
    #fmt.del_format(tool, film)