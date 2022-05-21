from os import R_OK
from readrnx_studenci import *
import numpy as np
import math
import linecache
from hirvonen import hirvonen

nav_file = './dane/nav.rnx'
obs_file = './dane/obs.rnx'

time_start =  [2022, 3, 21, 0, 0, 0]  
time_end =    [2022, 3, 21, 0, 0, 30] 

nav, inav = readrnxnav(nav_file)
obs, iobs = readrnxobs(obs_file, time_start, time_end, 'G')

# stale
maska = 10
u = 3.986005 * pow(10, 14)
we = 7.2921151467 * pow(10, -5)
c = 299792458.0 # predkosc swiatla

# usuniecie satelity 11
nav = np.delete(nav, np.where(inav == 11), axis=0)
inav = np.delete(inav, np.where(inav == 11))
obs = np.delete(obs, np.where(iobs[:,0] == 11))
iobs = np.delete(iobs, np.where(iobs[:,0] == 11), axis=0)

# usuniecie nan
iobs = np.delete(iobs, np.where(np.isnan(obs)), axis=0)
obs = np.delete(obs, np.where(np.isnan(obs)))

# najwazniejsze funkcje
def satpos(tobs, sat_idx, u, we, c):
    sat_id = sat_idx                                #2
    ind = (inav == sat_id)                          #3
    nav1 = nav[ind, :]                              #4

    dlg = len(nav1[:,17])
    t = np.full(dlg, tobs)                          #5                              
    toe_all = nav1[:,17]                            #6

    roznica = abs(toe_all - t)                      #7
    ind_t = np.argmin(roznica)                      #8   
    # print(f'{ind_t = }')

    nav0 = nav1[ind_t, :]                           #9

    # === === === === ===

    t0 = t[ind_t]                                   #10
    tk = t0 - nav0[17]

    a = pow(nav0[16],2)
    n0 = math.sqrt(u/pow(a,3))
    n = n0 + nav0[11]
    Mk = nav0[12] + n*tk
    Mk %= 2*math.pi

    Ek1 = Mk
    Ek = Mk + nav0[14]*math.sin(Ek1)
    while abs(Ek - Ek1) > 10**(-12):
        Ek1 = Ek
        Ek = Mk + nav0[14]*math.sin(Ek1)

    vk = math.atan2((math.sqrt(1-pow(nav0[14], 2))*math.sin(Ek)), (math.cos(Ek) - nav0[14]))
    if vk < 0:
        vk += 2 * math.pi

    phik = vk + nav0[23]

    delta_uk = nav0[15]*math.sin(2*phik) + nav0[13]*math.cos(2*phik)
    delta_rk = nav0[10]*math.sin(2*phik) + nav0[22]*math.cos(2*phik)
    delta_ik = nav0[20]*math.sin(2*phik) + nav0[18]*math.cos(2*phik)

    uk = phik + delta_uk
    rk = a*(1-nav0[14]*math.cos(Ek)) + delta_rk
    ik = nav0[21] + nav0[25]*tk + delta_ik

    xk = rk*math.cos(uk)
    yk = rk*math.sin(uk)

    omegak = nav0[19] + (nav0[24] - we)*tk - we*nav0[17]

    Xk = xk*math.cos(omegak) - yk*math.cos(ik)*math.sin(omegak)
    Yk = xk*math.sin(omegak) + yk*math.cos(ik)*math.cos(omegak)
    Zk = yk*math.sin(ik)

    r_kontrola = math.sqrt(pow(xk,2) + pow(yk,2))
    r_k = math.sqrt(pow(Xk,2) + pow(Yk,2) + pow(Zk, 2))
    test = abs(r_kontrola - r_k)
    # print(test)

    delta_t_s = nav0[6] + nav0[7]*(t0-nav0[17]) + nav0[8]*pow((t0-nav0[17]), 2)
    # uwaga tutaj w t0-toe+...

    delta_t_rel = ((-2*math.sqrt(u))/(pow(c,2)))*nav0[14]*nav0[16]*math.sin(Ek)
    delta_t_rel_s = delta_t_rel + delta_t_s

    return Xk, Yk, Zk, delta_t_rel_s
def popr_wsp(X0s, Y0s, Z0s, we, tau):
    wetau = we*tau
    matrix1 = np.array([[math.cos(wetau), math.sin(wetau), 0], [-math.sin(wetau), math.cos(wetau), 0], [0,0,1]])
    matrix2 = np.array([X0s, Y0s, Z0s])
    Xsrot = np.dot(matrix1, matrix2)
    return Xsrot
def azymut_elewacja_wys(wsp_obs, wsp_sat):
    wsp_obs_elips, h = hirvonen(wsp_obs) #zwracaj h, N = 40

    Xrs = np.transpose(np.array(wsp_obs - wsp_sat))
    
    fi = wsp_obs_elips[0]
    la = wsp_obs_elips[1]
    neu = np.array([[-math.sin(fi) * math.cos(la), -math.sin(la), math.cos(fi) * math.cos(la)],
                    [-math.sin(fi) * math.sin(la), math.cos(la), math.cos(fi) * math.sin(la)],
                    [math.cos(fi), 0, math.sin(fi)]])
    vNEU = np.dot(np.transpose(neu), Xrs)

    azymut = np.rad2deg(math.atan2(vNEU[1], vNEU[0]))
    if azymut < 0:
        azymut += np.rad2deg(2 * math.pi)
    if azymut >= 180:
        azymut -= 180
    
    elev = abs(np.rad2deg(math.asin(vNEU[2] / math.sqrt(vNEU[0] ** 2 + vNEU[1] ** 2 + vNEU[2] ** 2))))

    return azymut, elev, h
def tropo_hopfield(H, el):
    c1 = 77.64
    c2 = -12.96
    c3 = 3.718 * pow(10, 5)

    p0 = 1013.25
    t0 = 291.15
    Rh0 = 0.5
    N = 40

    h = H - N

    p = p0*pow((1-0.0000226), 5.225)
    t = t0 - 0.0065*h
    Rh = Rh0*math.exp(-0.0006396)
    e = 6.11*Rh*pow(10, ((7.5*(t-273.15))/(t-35.85)))

    Nd0 = c1*(p/t)
    Nw0 = c2*(e/t) + c3*(e/pow(t,2))
    N0 = Nd0 + Nw0

    hd = 40136 + 148.72*(t-273.15)
    hw = 11000

    tropo_w0 = ((pow(10, -6))/(5))*Nd0*hd
    tropo_d0 = ((pow(10, -6))/(5))*Nw0*hw

    mw_el = 1/(math.sin(np.deg2rad(pow(el, 2)) + 2.25))
    md_el = 1/(math.sin(np.deg2rad(pow(el, 2)) + 6.25))

    tropo_w = tropo_w0*mw_el
    tropo_d = tropo_d0*md_el

    tropo = tropo_w + tropo_d
    
    return tropo
def tropo_saastamoinen(H, el):
    p0 = 1013.25
    t0 = 291.15
    Rh0 = 0.5
    N = 40

    h = H - N

    p = p0*pow((1-0.0000226), 5.225)
    t = t0 - 0.0065*h
    Rh = Rh0*math.exp(-0.0006396)
    e = 6.11*Rh*pow(10, ((7.5*(t-273.15))/(t-35.85)))

    tropo_w0 = 0.002277*((1255/t)+0.05)*e
    tropo_d0 = 0.002277*p    

    tropo = (1/math.sin(np.deg2rad(el)))*(tropo_w0 + tropo_d0)

    return tropo
def bledy_wsp(XYZ_ref, XYZ_obl):
    def fun(a):
        return a - XYZ_ref

    bledy = np.apply_along_axis(fun, 1, XYZ_obl)

    #===

    # bledy_neu, h = hirvonen(bledy) #zwracaj h, N = 40
    
    # Xrs = np.transpose(np.array(XYZ_obl - XYZ_ref))

    # fi = bledy_neu[0]
    # la = bledy_neu[1]
    # neu = np.array([[-math.sin(fi) * math.cos(la), -math.sin(la), math.cos(fi) * math.cos(la)],
    #                 [-math.sin(fi) * math.sin(la), math.cos(la), math.cos(fi) * math.sin(la)],
    #                 [math.cos(fi), 0, math.sin(fi)]])
    # vNEU = np.dot(np.transpose(neu), Xrs)

    return bledy

# spisanie współrzędnych przybliżonych odbiornika z pliku OBS
XYZ_ref = ((linecache.getline(obs_file, 12)).split())[0:3]
XYZ_ref = [float(i) for i in XYZ_ref]
XYZ_ref = np.array(XYZ_ref)

# Przeliczenie daty początkowej i końcowej do sekund tygodnia GPS
week, tow = date2tow(time_start)[0:2]
week_end, tow_end = date2tow(time_end)[0:2]

# Otwieramy dużą pętlę
dt = 30

# def wsp_popr(tow, dt, obs, iobs, XYZ_ref, u, we, c, maska):
wsp_popr = np.empty((0,3))
for t in range(tow, tow_end+1, dt):

    sats_input = (iobs[ :,2] == t)
    sats = iobs[sats_input, 0]
    Pobs = obs[sats_input]

    wsp_obs = XYZ_ref
    delta_t_r = 0  
    tau = 0.072

    for i in range(3):
        y = np.empty((0,1))
        A = np.empty((0,4))
        for j, sat in enumerate(sats):
            tr = t + delta_t_r - tau
            X0s, Y0s, Z0s, delta_t_rel_s = satpos(tr, sat, u, we, c)
            Xsrot = popr_wsp(X0s, Y0s, Z0s, we, tau)
            ro_r_s = math.sqrt(pow((Xsrot[0] - wsp_obs[0]),2) + pow((Xsrot[1] - wsp_obs[1]),2) + pow((Xsrot[2] - wsp_obs[2]),2))
            # print(sat, ": ", ro_r_s)
            az, el, H = azymut_elewacja_wys(wsp_obs, Xsrot)
            tropo = tropo_hopfield(H, el)
            
            if el >= maska:
                Pcalc = ro_r_s - c*delta_t_rel_s + c*delta_t_r # + tropo # + jono
                y = np.append(y, np.array([Pcalc - Pobs[j]]))
                A_sat = np.array((-(Xsrot[0] - wsp_obs[0])/ro_r_s, -(Xsrot[1] - wsp_obs[1])/ro_r_s, -(Xsrot[2] - wsp_obs[2])/ro_r_s, 1))
                A = np.vstack((A, A_sat))
            
        Q = -np.linalg.inv(np.dot(A.T, A))
        Z = np.dot(Q, A.T)
        x = np.dot(Z, y)

        wsp_obs = np.add(wsp_obs, x[0:3])
        delta_t_r += x[3]/c
        tau = ro_r_s/c

    wsp_popr = np.vstack((wsp_popr, wsp_obs))
print(wsp_popr)
#     return wsp_popr
#             # print(tau, " ", X0s, " ", Y0s, " ", Z0s, '\n')

# XYZ_obl = wsp_popr(tow, dt, obs, iobs, XYZ_ref, u, we, c, maska)
# bledy = bledy_wsp(XYZ_ref, XYZ_obl)
# np.savetxt('test.txt', bledy, delimiter=', ', fmt='%1.8f')
# === === === === === SPP