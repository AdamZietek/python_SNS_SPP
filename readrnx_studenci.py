
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 20:39:35 2020

@author: Maciek
"""
import numpy as np
from datetime import date


''' RINEX NAWIGACYJNY'''

def readrnxnav(file):
    m=1
    nav=np.zeros((2000,37))
    inav=np.zeros((2000))
    n=-1
    with open(file, "r") as f:
        for s in f:                
            answer = s.find('END OF HEADER') # skip header
            if answer != -1:
                break
        for s in f:
            s = s.replace('D', 'E')
            if m==1:
                prn=int(s2n(s,1,2))
                a = np.empty((1,6))
                a[:] = np.NaN
                a[0,0:6]=np.array(s2e(s,4,23))
            else:
                a=np.append(a,s2n(s,4,19))
            for x in range (3):
                p=23+x*19
                a=np.append(a,s2n(s,p,19))
            if m<8:
                m+=1
            else:
                n+=1
                nav[n,:]=a
                inav[n]=prn
                m=1
        nav=nav[0:n+1,:]
        inav=inav[0:n+1]
        inav = inav.astype(int)
    f.close()
    return nav, inav

def readrnxobs(file, time_start, time_end, GNSS = 'G'):
    with open(file, "r") as f: 
        for s in f:
            label = s[59:]
            if label.find('SYS / # / OBS TYPES') == 1:
                if s[0] == GNSS:
                    p = 7
                    types_header = []
                    for i in range(int(s[4:4+2])):
                        if p > 58:
                            p = 7
                            s = next(f)
                        types_header.append(s[p:p+3])
                        p += 4
                
            elif label.find('END OF HEADER') == 1:
                break
            types_of_obs = ['C1C']
            # types_of_obs = ['C1C', 'C2W']
        ind = np.zeros((len(types_header)))
        for n in range(len(types_of_obs)):
            i=(types_header.index(types_of_obs[n])) if types_of_obs[n] in types_header else -1#np.empty((0))
            if i>-1:
                ind[i]=n+1
        
        obs = np.zeros((150000, len(types_of_obs)))*np.nan
        iobs = np.zeros((150000, 3))
        n = 0
        for s in f:
            label = s[0]
            if label == '>':
                epoch = s2e(s,2,29)
                y = epoch[0]
                # tt = (date.toordinal(date(epoch[0],epoch[1],epoch[2]))+366-t0)*86400+np.dot((epoch[3:6]), ([3600,60,1])) + 6*86400
                tt = date2tow(epoch)[1] - date2tow(epoch)[2] * 86400
                if tt > (date2tow(time_end)[1] - date2tow(epoch)[2] * 86400):
                    break
                else:
                    flag = int(round(tt))>=(date2tow(time_start)[1] - date2tow(time_start)[2] * 86400)
                if flag:
                    number_of_all_sats = int(s[33:33+2])
                    iobs[n+np.arange(0,number_of_all_sats),1] = tt
                    iobs[n+np.arange(0,number_of_all_sats),2] = date2tow(epoch)[1]
                    for sat in range(number_of_all_sats):
                        s = next(f)
                        p = 3
                        if s[0] == GNSS:
                            for i in range(len(types_header)):
                                if ind[i] != 0:
                                    obs[n+sat, int(ind[i] - 1)] = s2n(s,p,16)
                                    iobs[n+sat,0] = s2n(s,1,2)
                                p+=16
                    n += number_of_all_sats
        obs = obs[0:n, :]
        iobs = iobs[0:n,:]
        obs = np.delete(obs,iobs[:,0]==0, axis=0)
        iobs = np.delete(iobs,iobs[:,0]==0, axis=0)
        f.close()
        iobs = iobs.astype(int)
    return obs, iobs

def s2e(s,p,n):
    epoch = [int(s[p:p+4]), int(s[p+5:p+5+2]), int(s[p+8:p+8+2]), int(s[p+11:p+11+2]), int(s[p+14:p+14+2]), float(s[p+17:n])]
    return epoch 

def date2tow(data):    
    dday=date.toordinal(date(data[0],data[1],data[2])) - (date.toordinal(date(1980,1,6)))
    week = dday//7
    dow = dday%7
    tow = dow * 86400 + data[3] * 3600 + data[4] * 60 + data[5]
    return week, tow, dow

def s2n(s,p,n):
    a = s[p:p+n]
    if (not (a and not a.isspace())):
        a = np.nan
    else:
        a = float(a)        
    return a