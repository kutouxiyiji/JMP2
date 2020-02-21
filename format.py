# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 16:16:43 2020

@author: YWu
"""

import pickle
class Format:
    
    def __init__(self, path='', filename = 'format_dict'): # my path C:/Users/ywu156243/Documents/Yong Wu/Python/Test/JMP/
        self.formatdic = self.load_obj(path, filename)
                
    def load_obj(self, path,name):
        with open(path + name + '.pkl', 'rb') as f:
            return pickle.load(f)
    
    def save_obj(self, path='', name = 'format_dict'):
        obj = self.formatdic
        with open(path + name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
                
    def create_new_format(self, tool, film, pts, cols, rows):
        key = (tool, film)
        self.formatdic[key] = [pts,cols,rows]
        self.save_obj()
    
    def read_format_dict(self):
        return self.formatdic
    
    def del_format(self, tool, film):
        key = (tool, film)
        del self.formatdic[key]
        self.save_obj()