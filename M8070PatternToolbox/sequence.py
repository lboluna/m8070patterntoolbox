# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 16:45:30 2020

@author: luis.boluna@keysight.com


Sequence

Is a repository of tools for the manipulation of digital sequences.


"""

    
def gray(sequence):
    """
    gray(sequence)

    Parameters
    ----------
    sequence : TYPE string
        DESCRIPTION.
        
        applies gray code mapping to the passed binary sequence and returns a 
        PAM-4 symbol based sequence.
        
        No error checking. Make sure you have even numbered binary sequences

    Returns
    -------
    prbspam : TYPE string
        DESCRIPTION.
        
        PAM-4 symbol based sequence that is gray coded.

    """
    
    gry = {'00': '0', '01': '1', '11':'2', '10':'3'}
    y = [sequence[i:i+2] for i in range(0,len(sequence),2)]  # grab string in blocks of two chars and place into list
    prbspam = ''
    for x in enumerate(y):
        prbspam += (gry[x[1]])
    return prbspam

def ungray(sequence):
    """
    ungray(sequence)

    Parameters
    ----------
    sequence : TYPE string
        DESCRIPTION.
        
        unmaps and removes gray code mapping to the passed PAM-4 symbol based
        sequence and returns a binary based sequence.
        
        No error checking. 

    Returns
    -------
    prbspam : TYPE string
        DESCRIPTION.
        
        binary sequence

    """
    ugry = {'0':'00', '1':'01', '2':'11', '3':'10'}
    prbspam = ''
    for x in enumerate(sequence):
        prbspam += (ugry[x[1]])
    return prbspam

def enc_PAM4_to_bin(sequence):
    """
    enc_PAM4_to_bin(sequence)

    Parameters
    ----------
    sequence : TYPE String
        DESCRIPTION.
        
        Encodes a PAM-4 based symbol sequence from a binary sequence.
        
        Note that no error checking. Needs to ensure that binary sequence is 
        even in length.

    Returns
    -------
    prbspam : TYPE String
        DESCRIPTION.

    binary based sequence
    
    """
    
    enc = {'0':'00', '1':'01', '2':'10', '3':'11'}
    prbspam = ''
    for x in enumerate(sequence):
        prbspam += (enc[x[1]])
    return prbspam

def enc_bin_to_PAM4(sequence):
    """
    enc_bin_to_PAM4(sequence)

    Parameters
    ----------
    sequence : TYPE String
        DESCRIPTION.
        
        Encodes a binary sequence to A PAM-4 symbol based sequence.
        
        Note that no error checking. Needs to ensure that binary sequence is 
        even in length.

    Returns
    -------
    prbspam : TYPE String
        DESCRIPTION.

    PAM-4 symbol based sequence
    
    """
    
    enc = {'00': '0', '01': '1', '10':'2', '11':'3'}
    y = [sequence[i:i+2] for i in range(0,len(sequence),2)]  # grab string in blocks of two chars and place into list
    prbspam = ''
    for x in enumerate(y):
        #print(y)
        prbspam += (enc[x[1]])
    return prbspam

def flip(sequence):
    """
    
    flip(sequence)

    Parameters
    ----------
    sequence : TYPE String 
        DESCRIPTION.
        
        Flips order of sequence
        
        Sequence agnostic. Can be binary,or PAM-N

    Returns
    -------
    TYPE String
        DESCRIPTION.
        
        Sequence is returned in orginal symbol type

    """
    return sequence[::-1]

def invert(sequence):
    """
    invert that determines if NRZ or PAM4 then inverts
    
    Parameters
    ----------
    sequence : TYPE String
        DESCRIPTION.
        
        inverts the sequence

    Returns
    -------
    None.

    """
    pass

def numpy2sequence(numpyarr):
    """
    numpy2sequence(numpyarr)

    Parameters
    ----------
    numpyarr : TYPE Numpy array
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    return numpyarr.tolist()

def makecomma(sequence):
    """
    makecomma(sequence)
    
    Parameters
    ----------
    sequence : string
        This is a sequnce of binary or binary encoded bit

    Returns
    -------
    None.

    
    Returns sequence formatted with commas
    
    sequence is a string
    Returned value is a string
      
    """
    return ",".join(sequence)

def shiftLbyn(sequence,n=0):
    """
    shiftLbyn(arr, n=0)
    
    Returns circular shifted by n to the Left sequence 
    
    arr is a string
    n is an integer
    Returned value is a string
      
    """
    return sequence[n::] + sequence[:n:]

def shiftRbyn(sequence,n=0):
    """
    shiftRbyn(arr, n=0)
    
    Returns circular shifted by n to the Right sequence 
    
    arr is a string
    n is an integer
    Returned value is a string
      
    """
    return sequence[n:len(sequence):] + sequence[0:n:]

def invertBIN(sequence):
    """
    invertPAM(sequence)
    
    Returns inverted PAM-4 sequence
    
    Sequence is a string of PAM-4 based symbols [0,1,2,3]
    Returned value is a string of PAM-4 based symbols [0,1,2,3]
      
    """
    pattern = ''
    tmp = ''
    for pidx in range(0, len(sequence)):
        if(sequence[pidx] == '0'):
            tmp = '1'
        elif (sequence[pidx] == '1'):
            tmp = '0'
        pattern = pattern + tmp
    return pattern

def invertPAM4(sequence):
    """
    invertPAM(sequence)
    
    Returns inverted PAM-4 sequence
    
    Sequence is a string of PAM-4 based symbols [0,1,2,3]
    Returned value is a string of PAM-4 based symbols [0,1,2,3]
      
    """
    pattern = ''
    tmp = ''
    for pidx in range(0, len(sequence)):
        if(sequence[pidx] == '0'):
            tmp = '3'
        elif (sequence[pidx] == '1'):
            tmp = '2'
        elif (sequence[pidx] == '2'):
            tmp = '1'
        elif (sequence[pidx] == '3'):
            tmp = '0'
        pattern = pattern + tmp
    return pattern

def precode(sequence, **kwargs):    #CL 94.2.2.6
    """
    precode(sequence)
    
    Returns precode value of PAM-4 sequence using the precoder definition is 
    IEEE Clause 94.2.2.6
    
    Note that the modulus looks like 1/(1+D) precode = (input[t]-output[t-1])%4
    
    sequence string of PAM-4 symbols [0,1,2,3]
    Return value s a string of PAM-4 symbols [0,1,2,3]
    
    """
    #
    # April 2023: Added kwargs with init to debig precode initialization. If sequence[0]
    #    then correlates to Sudeep result in IEEE slide but does not correlate with M8070
    #    precode.
    #
    
    first = kwargs.get("init", sequence[0])
#     pre = ''
#     prev = 0
# #    tx = 0
# #    p = 0
#     for idx in range(0,len(sequence)):
#         if idx == 0:
#             p = sequence[idx]
#         else:
#             tx = str(int(sequence[idx]) - int(prev))
#             p = str(int(tx)%4)
#         pre = pre + p
#         prev = p
#         print(" t= %s, P(t) = (G(t)=%s - P(t-1)=%s)%%4 = %s ::: pre=%s" %(str(idx), sequence[idx],prev, p, pre))

    precode = '' #empty out string for use.
    #init = sequence[0]
    delay = first
    
    for idx in range(0,len(sequence)):
    
        plus = str(int(sequence[idx]) - int(delay))
        p = str(int(plus)%4)
        precode = precode + p 
        delay = p
 
    return precode

def unprecode(sequence):
    """
    unprecode(sequence)
    
    Returns reverse precoded value of a PAM-4 sequence
    
    Note, (1+D) precode - uncodes 1/(1+D) - need to run this before
    "ungraying" patt 
    = (input[t]+output[t-1])%4
    
    sequence string of PAM-4 symbols [0,1,2,3]
    Return value s a string of PAM-4 symbols [0,1,2,3]
    
    """
    
    tmp = sequence[0]
    #unpre = str((int(sequence[1]) + int(tmp))%4)
    unpre = tmp
    for idx in range(1, len(sequence)):
        tx = str(int(sequence[idx]) + int(tmp))
        r = str(int(tx)%4)
        unpre = unpre + r
        #print("(%s+%s)mod4= %s  unpre = %s" %(tmp, sequence[idx], r, unpre))
        tmp = sequence[idx]
    return unpre

    def xorpatt(pat1, pat2):
        result = ""
        count = 0
        total = 0
        for x,y in zip(pat1,pat2):
            total += 1
            if x == y:
                result = result + "0"
            else:
                result = result + "1"
                count += 1
        return result, float(count/total)
                
        
    def printtable(header,data):
    #    header = ["Man Utd", "Man City", "T Hotspur"]
    #    data = np.array([[1, 2, 1],
    #                 [0, 1, 0],
    #                 [2, 4, 2]])
        
        row_format ="{:>15}" * (len(header) + 1)
        print(row_format.format("", *header))
        for head, row in zip(header, data):
            print(row_format.format(head, *row))
        return