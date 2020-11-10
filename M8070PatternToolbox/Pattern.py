# -*- coding: utf-8 -*-
"""
Created on Tues Sep 17 13:48:49 2019

@author: luis.boluna@keysight.com

Class to work with M8070 Pattern files.

Basic class geared towards the reading and writing of Keysight M8070 pattern
files for use in their BERTs and AWGs. IQTools support planned as well.
    

    
    To use:
        
        pdata = pattern()
        pdata.readptrn(PTRN_FILENAME)

        pdata.properties
        
    Sample result:    
        
        symbol length is 13116
        mask is False
        squelch is False
        pack is 1 bits
        symbol is BIT
        Version is M8000 1.0.0
        First 10 symbols of data is 0110000110
                
    
    To view the data:
        
        pdata.data
    
    Sample result:
        
        '0100100110110011110001010101100001001001110111100111010000 ....
                   ... 011101001101110100111001100101011100011111110101110'
    

Some basic error checking and exceptions have been implemented.

"""

class pattern(object):
    
    def __init__(self):
        self.mask = False
        self.squelch = False
        self.error = False 
        self.description = ''
        self.version = 'M8000 1.0.0'
        self.symbol = 'BIT'
        self.pack = 1
        self.data = '0001'
        self.name = 'default'
        self.length = len(self.data)
        return
    

    @staticmethod
    def onNoff(item):
        if item == 'ON':
            return '1'
        elif item == 'OFF':
            return '0'
        elif (item == '1' or item == '0'):
            return item
        else:
            raise(Exception("Incorrect format: not ON, OFF, 1 or 0"))        
            
        
    def readptrn(self,filename):
        """
        readptrn
    

        Parameters
        ----------
        filename : TYPE String
            DESCRIPTION.
            
            Method to read M8070 pattern files. With some basic error checking.

        Returns
        -------
        
        Appends pattern to self.data
        Appends name to self.name
        Appends version to self.version
        Appends pattern symbol length to self.length
        Appends ptrn symbol type to self.symbol
        Appends ptrn mask bit to self.mask
        Appends ptrn squelch bit to self.squelch
        Appends ptrn error bit to self.error
        Appends ptrn pack type to self.pack

        """
        symbolcoding = ['BIT','B810B','B128BB130','B128B132']
        vers = ['M8000 1.0.0', 'M8000 1.0.1']
        packed = ['1','4','8']
        
        with open(filename) as f:
            self.name = filename.split(".")[0].strip("\n")
            for line in iter(f.readline, ''):
                if line.startswith("Version="):
                    if line.split("=")[1].strip("\n") in vers:
                        self.version = line.split("=")[1].strip("\n")
                    else:
                        raise(Exception("Incorrect version type in pattern file Version= line"))
                elif line.startswith("Use="):
                    contents = line.split("=")[1].strip("\n")
                    use = contents.split(",")
                    for i,element in enumerate(use):
                        if i == 0:
                            self.length =  int(element)
                        elif i == 1:
                            if element in symbolcoding:
                                self.symbol = element
                            else:
                                raise(Exception("Incorrect symbol type in pattern file Use= line"))
                        elif i == 2:
                            self.mask = bool(int(self.onNoff(element)))
                        elif i == 3:
                            self.squelch = bool(int(self.onNoff(element)))
                        elif i == 4:
                            self.error = bool(int(self.onNoff(element)))
                        else:
                            raise(Exception("Syntax Error in pattern file Use= line"))
                elif line.startswith("Description="):
                    self.description = line.split("=")[1]
                elif line.startswith("Pack="):
                    if line.split("=")[1].strip("\n") in packed:
                        self.pack = int(line.split("=")[1])
                    else:
                        raise(Exception("Incorrect bits in pattern file Pack= line"))
                elif line[0].isdigit():
                    self.data = line
                elif line.startswith("Data="):
                    pass
                else:
                    raise(Exception("Syntax Error in pattern file line:: {}".format(line)))
                    
        if self.error:
            if self.mask and self.squelch:
                raise(Exception("Pattern file Error:: If ERROR=1 then MASK=0 and SQUELCH=0"))
                
            
                    
    def writeptrn(self, filename):
        """
        
        writeptrn

        Parameters
        ----------
        filename : TYPE String
            DESCRIPTION.
            
            Method to write M8070 pattern files of data patterns. These files
            can then be used on M8070 supported equipment. 
            
            Uses:
                
            pattern to self.data
            name to self.name
            version to self.version
            pattern symbol length to self.length
            ptrn symbol type to self.symbol
            ptrn mask bit to self.mask
            ptrn squelch bit to self.squelch
            ptrn error bit to self.error
            ptrn pack type to self.pack    

        Returns
        -------
        
        A M8070 pattern file withn the ptrn extension as FILENAME.ptrn

        """
        symbolcoding = ['BIT','B810B','B128BB130','B128B132']
        vers = ['M8000 1.0.0', 'M8000 1.0.1']
        packed = ['1','4','8']
        
        self.length = len(self.data)
        if self.symbol in symbolcoding:
            use = str(self.length)+','+str(self.symbol)+','
            use = use + str(int(self.mask)) 
            use = use+','+str(int(self.squelch)) if int(self.squelch) > 0 else use+',0'
            use = use+','+str(int(self.error)) if int(self.error) > 0 else use+''
        else:
            raise(Exception("ERROR: symbol is invalid, cannot write pattern file:: {}".format(self.symbol)))
        
        if filename[-5:] != '.ptrn':
            filename = filename + '.ptrn'
            
        with open(filename, 'w') as f:
            if self.version in vers:
                 f.write('Version={}\n'.format(self.version))
            else:
                 raise(Exception("ERROR: Incorrect version, cannot write pattern file:: {}". format(self.version)))
            f.write('Use={}\n'.format(use))
            if self.description:
                f.write('Description={}\n'. format(self.description))
            if str(self.pack) in packed:
                f.write('Pack={}\n'.format(str(self.pack)))
            else:
                raise(Exception("ERROR: Incorrect packed, cannot write pattern file:: {}",format(self.pack)))
            f.write('Data=\n')
            if self.data:
                f.write(self.data +'\n')
            else:
                raise(Exception("ERROR: Data is empty, cannot wite pattern file"))
    
        print("Data pattern:{} written to {}".format(self.name, filename))
        return
        
    @property
    def properties(self):
        print("symbol length is {}".format(self.length))
        print("mask is {}".format(self.mask))
        print("squelch is {}".format(self.squelch))
        print("pack is {} bits".format(self.pack))
        print("symbol is {}".format(self.symbol))
        print("Version is {}".format(self.version))
        print("First 10 symbols of data is {}".format(self.data[0:10]))
        return
    

    
            
if __name__ == "__main__":

    pattfile = "PRBS13Q.ptrn"
    pdata = pattern()
    pdata.readptrn(pattfile)

    pdata.properties
    


    
    
    

        