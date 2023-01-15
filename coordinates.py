# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 12:24:13 2020
@author: Eimantas
"""


class coordinates:
    def __init__(self, imput):
        self.imput=imput
        
    def corrected(self):
        imput=self.imput
        if abs(imput[0]-imput[2])<5 and abs(imput[0]-imput[2])<5:
            new=(imput[0]-20,imput[1]-20,40,40)
            
        if imput[2]-imput[0]>0 and imput[3]-imput[1]>0:
            new=(imput[0], imput[1], imput[2]-imput[0], imput[3]-imput[1])
            
        if imput[2]-imput[0]<0 and imput[3]-imput[1]<0:
            new=(imput[2], imput[3], imput[0]-imput[2], imput[1]-imput[3])
            
        if imput[2]-imput[0]>0 and imput[3]-imput[1]<0:
            new=(imput[0], imput[3], imput[2]-imput[0], imput[1]-imput[3])
            
        if imput[2]-imput[0]<0 and imput[3]-imput[1]>0:
            new=(imput[2], imput[1], imput[0]-imput[2], imput[3]-imput[1])
        
        return new