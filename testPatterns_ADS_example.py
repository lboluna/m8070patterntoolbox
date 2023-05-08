# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 16:38:32 2020

@author: luis.boluna@keysight.com

Example code using the M8070PatternToolbox

Purpose is to write patterns for use inside of ADS 

"""

import numpy as np
import M8070PatternToolbox as pat

def writeADSpatt(filename, data):
        with open(filename, 'w') as f:
            f.write(data)
        print("File: {:} created".format(filename))
        

if __name__ == '__main__':
    
    filename = 'QPRBS13-CEI_'
    qprbs13 = pat.Pattern.pattern()
    qprbs13.readptrn('C:\\Users\\luboluna\\Documents\\Disk\\python\\m8070patterntoolbox\\patterns_m8070\\QPRBS13-CEI_bit.ptrn')
    x = qprbs13.data
    y = pat.sequence.gray(x)
    writeADSpatt(filename+'PAM4.txt', y)
    writeADSpatt(filename+'NRZ.txt', pat.sequence.enc_PAM4_to_bin(y))