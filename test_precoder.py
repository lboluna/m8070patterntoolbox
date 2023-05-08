# -*- coding: utf-8 -*-
"""
Created on Mon May  1 13:13:35 2023

@author: luboluna
"""

import numpy as np
import M8070PatternToolbox as pat

Sudeep_Input_Sequence =          "2222032013300002303"
Sudeep_Precode_Output_Sequence = "0202211321222220312"


test = pat.Pattern.pattern()
test.name = 'SudeepPrecode'
test.data = pat.sequence.precode(Sudeep_Input_Sequence)
test.length = len(test.data)
test.properties

if test.data == Sudeep_Precode_Output_Sequence:
    print("\n\nMATCHES\n")
    

test2 = pat.Pattern.pattern()
test2.name = 'SudeepPrecode'
test2.data = pat.sequence.precode("0"+Sudeep_Input_Sequence+"0")
test2.length = len(test2.data)
test2.properties

