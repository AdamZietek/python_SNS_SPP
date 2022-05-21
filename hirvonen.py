# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 10:09:31 2021

@author: Maciek
"""

import numpy as np
import math as mat

a = 6378137
e2 = 0.00669438002290

def Np(B):
    N = a/(1-e2*(np.sin(B)**2))**0.5
    return N

def hirvonen(arr):

    X = arr[0]
    Y = arr[1]
    Z = arr[2]

    r = (X**2 + Y**2)**0.5
    B = mat.atan(Z/(r*(1-e2)))
    
    while 1:
        N = Np(B)
        H = r/np.cos(B) - N
        Bst = B
        B = mat.atan(Z/(r*(1-(e2*(N/(N+H))))))    
        if abs(Bst-B)<(0.00001/206265):
            break
    L = mat.atan(Y/X)
    N = Np(B)
    H = r/np.cos(B) - N

    elips = np.array((B,L,H))
    return elips, H