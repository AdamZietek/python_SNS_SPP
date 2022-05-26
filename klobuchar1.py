# -*- coding: utf-8 -*-
"""
Created on Thu May 26 10:39:15 2022

@author: mgrzy
"""

import numpy as np
import math

c = 299792458.0
def klobuchar(tow, phi, lam, el, az, alfa, beta, c):
    '''
    
    Parameters
    ----------
    tow : float/int
        Time of Week - czas tygodnia GPS obserwacji
    phi : float [degrees]
        szerokosć geodezyjna odbiornika
    lam : float [degrees]
        długosć geodezyjna odbiornika
    el : float [degrees]
        elewacja satelity
    az : float [degrees]
        azymut satelity
    alfa : list/np.array - 4-elemntowa lista
        współczynniki alfa modelu Klobuchara
    beta : list/np.array - 4-elemntowa lista
        współczynniki beta modelu Klobuchara

    Returns
    -------
    dI : float
        poprawka jonosferyczna w kierunku satelity

    '''      
    
    # zamiana jednostek ze stopni do półłuków - semicircles
    deg2sem = 1/180
    sem2rad = 1*np.pi
    els = el*deg2sem

    psi = 0.0137/(els + 0.11) - 0.022
    
    phi_ipp = phi*deg2sem + psi*np.cos(np.deg2rad(az))

    if phi_ipp > 0.416:
        phi_ipp = 0.416
    elif phi_ipp < -0.416:
        phi_ipp = -0.416

    lam_ipp = (lam*deg2sem) + (psi*np.sin(np.deg2rad(az)))/np.cos(phi_ipp*np.pi)
    
    phi_m = phi_ipp + 0.064 * np.cos((lam_ipp - 1.617)*np.pi)

    t = 43200 * lam_ipp + tow

    # t = math.fmod(t, 86400)
    t %= 86400

    if t < 0:
        t += 86400
    # if t >= 86400:
    #     t -= 86400
    # elif t < 0:
    #     t += 86400

    aion = alfa[0] + alfa[1]*phi_m + alfa[2]*math.pow(phi_m, 2) + alfa[3]*math.pow(phi_m, 3)

    if aion < 0:
        aion = 0

    pion = beta[0] + beta[1]*phi_m + beta[2]*math.pow(phi_m, 2) + beta[3]*math.pow(phi_m, 3)

    if pion < 72000:
        pion = 72000

    phi_ion = 2*np.pi*(t-50400)/pion

    mf = 1 + 16*math.pow((0.53-els), 3)

    if abs(phi_ion) <= np.pi/2:
        dI = c * mf * (5*10**(-9) + aion*(1-phi_ion**2/2 + phi_ion**4/24))
    elif abs(phi_ion) > np.pi/2:
        dI = c * mf * 5 * 10**(-9)

    return dI

if __name__ == '__main__':

    alfa = [1.6764e-08,  7.4506e-09, -1.1921e-07,  0.0000e+00]
    beta = [1.1059e+05,  0.0000e+00, -2.6214e+05,  0.0000e+00] 
    
    B = 50.4749
    L = 20.0352

    el = 30
    az = 20

    tow = 86400/2
    diono = klobuchar(tow, B, L, el, az, alfa, beta, c)
    print(diono)

