# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 16:38:32 2020

@author: luis.boluna@keysight.com

Example code using the M8070PatternToolbox

"""

import numpy as np
import M8070PatternToolbox as pat



if __name__ == '__main__':
    
    #Create prbs13q per 120.5.121.2.1::
    fpoly = [13,12,2,1]
    fcoeff = [1,1,1,1]
    state = np.array([0,0,0,0,0,1,0,1,0,1,0,1,1])
    L1 = pat.pylfsr2.LFSR(fpoly=fpoly,fcoeff = fcoeff , initstate=state, verbose=False)
    #L1.info()
    L1.runFullCycle()
    
    prbs13bin = ''
    for y in enumerate(L1.seq.tolist()):
         prbs13bin += str(y[1])
    
    prbs13bin2 = prbs13bin+prbs13bin #spec says to repeat pattern twice so even number of symbols
    prbs13pamg = pat.sequence.gray(prbs13bin2) #graycoded pam-4
   
  
    # Save PRBS13Q to test file as M8070 ptrn file
    prbs13ptrn = pat.Pattern.pattern()
    prbs13ptrn.name = 'PRBS13Q'
    prbs13ptrn.data = prbs13bin+prbs13bin
    prbs13ptrn.length = len(prbs13bin2)
    prbs13ptrn.properties
    prbs13ptrn.writeptrn('PRBS13Q.ptrn')
    
    print("\n\nPRBS13Q in NRZ, no gray coded {} symbols long:\n{}".format(prbs13ptrn.length,prbs13bin2))
    print("\n\nPRBS13Q in PAM-4, gray coded {} symbols long:\n{}".format(len(prbs13pamg),prbs13pamg))
    prbs13bing = pat.sequence.enc_PAM4_to_bin(prbs13pamg)
    print("\n\nPRBS13Q in NRZ, gray coded {} symbols long:\n{}".format(len(prbs13bing),prbs13bing))
    prbs13pam = pat.sequence.enc_bin_to_PAM4(prbs13bin2)
    print("\n\nPRBS13Q in PAM-4, not gray coded {} symbols long:\n{}".format(len(prbs13pam),prbs13pam))
    
    