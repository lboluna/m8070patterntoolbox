# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 12:14:21 2023

@author: luboluna
"""

sequence = '2222032013300002303'
result   = '0202211321222220312'

    
precode = '' #empty out string for use.
init = sequence[0]
delay = sequence[0]

for idx in range(0,len(sequence)):

    plus = str(int(sequence[idx]) - int(delay))
    p = str(int(plus)%4)
    precode = precode + p 
    delay = p
    if p == result[idx]:
        check = '-'
    else:
        check = 'X'
    print(f"idx: {idx+1}\t {sequence[idx]}\t {plus}\t {p}\t {check}  {result[idx]}\t {delay}")
    