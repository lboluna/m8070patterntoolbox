# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 16:38:32 2020

@author: luis.boluna@keysight.com

Example code using the M8070PatternToolbox

Purpose of this code is to create patterns to be used by M819X AWG.

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
    
    prbs13bin2 = prbs13bin+prbs13bin #spec says to repeat pattern twice so even number of symbols
    prbs13pamg = pat.sequence.gray(prbs13bin2) #graycoded pam-4
   
  
    # Save PRBS13Q to test file as M8070 ptrn file
    prbs13ptrn = pat.Pattern.pattern()
    prbs13ptrn.name = 'PRBS13Q'
    prbs13ptrn.data = prbs13bin+prbs13bin
    prbs13ptrn.length = len(prbs13bin2)
    prbs13ptrn.properties
    prbs13ptrn.writeptrn('PRBS13Q.ptrn')
    
    print()
    
    # PRBS13Q Gray Coded
    prbs13bing = pat.sequence.enc_PAM4_to_bin(prbs13pamg)
    prbs13Grayptrn = pat.Pattern.pattern()
    prbs13Grayptrn.name = 'PRBS13Q_GrayCoded'
    prbs13Grayptrn.data = prbs13bing
    prbs13Grayptrn.length = len(prbs13bing)
    prbs13Grayptrn.properties
    prbs13Grayptrn.writeptrn('PRBS13Q_GrayCoded.ptrn')
    
    print()
    
    # below commented out... debugging issue found on precode - LB 4/19/2023
    # PRBS13Q Gray Coded & Precode
    prbs13GrayP = pat.sequence.precode(prbs13pamg, first = "3")   #
    prbs13bingpre = pat.sequence.enc_PAM4_to_bin(prbs13GrayP)
    prbs13GrayPreptrn = pat.Pattern.pattern()
    prbs13GrayPreptrn.name = 'PRBS13Q_GrayCodedPrecode'
    prbs13GrayPreptrn.data = prbs13bingpre
    prbs13GrayPreptrn.length = len(prbs13bingpre)
    prbs13GrayPreptrn.properties
    prbs13GrayPreptrn.writeptrn('PRBS13Q_GrayCodedPrecodeThree.ptrn')
    