# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 16:38:32 2020

@author: luis.boluna@keysight.com

Example code using the M8070PatternToolbox

Purpose of this code is an attempt to create patterns that are created by 
IQTools where the AUTO next to sample rate is not enabled/checked. The overflow
is aded to the pattern and based on user's length input.

"""

import numpy as np
import M8070PatternToolbox as pat



if __name__ == '__main__':
    
#    Create prbs13q per 120.5.121.2.1::
    fpoly = [13,12,2,1]
    fcoeff = [1,1,1,1]
    state = np.array([0,0,0,0,0,1,0,1,0,1,0,1,1])
    L1 = pat.pylfsr2.LFSR(fpoly=fpoly,fcoeff = fcoeff , initstate=state, verbose=False)
    #L1.info()
    L1.runFullCycle()
    
    prbs13bin = ''
    for y in enumerate(L1.seq.tolist()):
          prbs13bin += str(y[1])
    
    prbs13bin2 = prbs13bin+pat.sequence.invertBIN(prbs13bin) #spec says to repeat pattern twice so even number of symbols
    prbs13pamg = pat.sequence.gray(prbs13bin2) #graycoded pam-4
   
  
    # Save PRBS13Q to test file as M8070 ptrn file
    # prbs13ptrn = pat.Pattern.pattern()
    # prbs13ptrn.name = 'PRBS13Q'
    # prbs13ptrn.data = prbs13bin+prbs13bin
    # prbs13ptrn.length = len(prbs13bin2)
    # prbs13ptrn.properties
    #prbs13ptrn.writeptrn('newPRBS13Q.ptrn')
    
    symbols = int( input('Enter Number of Symbols you see in IQTools = ') )
    prbs_length = len(prbs13pamg)
    prbs_spillover = symbols%prbs_length
    prbs_repeat = int((symbols-prbs_spillover)/prbs_length)
    resulting_pattern = (prbs13pamg*prbs_repeat)+prbs13pamg[-prbs_spillover:]
    print(f"\n\nPRBS13Q in PAM-4, gray coded {len(resulting_pattern)} symbols long:\n{resulting_pattern}")
    print('\n\n')
    
    # Save PRBS13Q to test file as M8070 ptrn file
    result = pat.Pattern.pattern()
    result.name = 'IQTools_PRBS13Q'
    ung_result = pat.sequence.ungray(resulting_pattern)
    result.data = pat.sequence.enc_bin_to_PAM4(ung_result)
    result.length = len(result.data)
    result.properties
    result.writeptrn('IQTools_PRBS13Q.ptrn')
