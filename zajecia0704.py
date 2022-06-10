from readrnx_studenci import *
from utils import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

nav_file = './kod/nav.rnx'
obs_file = './kod/obs.rnx'

time_start =  [2022, 3, 21, 0, 0, 0]
time_end =    [2022, 3, 21, 4, 10, 0] 

nav, inav = readrnxnav(nav_file)
obs, iobs = readrnxobs(obs_file, time_start, time_end, 'G')

# stale
maska = 10
u = 3.986005 * pow(10, 14)
we = 7.2921151467 * pow(10, -5)
c = 299792458.0
dt = 30
alfa, beta = alfa_beta(nav_file)

XYZ_ref = wsp_odbiornika(obs_file)
nav, inav, obs, iobs = porzadek(nav, inav, obs, iobs)

week, tow = date2tow(time_start)[0:2]
week_end, tow_end = date2tow(time_end)[0:2]

XYZ_obl, czas, l_sats, GDOP, PDOP, TDOP, HDOP, VDOP = wsp_popr(tow, tow_end, inav, nav, alfa, beta, dt, obs, iobs, XYZ_ref, u, we, c, maska)
XYZ_bledy, NEU_bledy = bledy_wsp(XYZ_ref, XYZ_obl)
np.savetxt('./wyniki/test.txt', XYZ_bledy, delimiter=', ', fmt='%1.8f')

std_dev, mean_square_err, min_val, max_val = analiza_bledow(XYZ_bledy)
std_dev_neu, mean_square_err_neu, min_val_neu, max_val_neu = analiza_bledow(NEU_bledy)

# wykres_bledow(czas, XYZ_bledy, "xyz")
# wykres_bledow(czas, NEU_bledy, "neu")
# wykres_l_sats(czas, l_sats)
wykres_punktowy_n_e(NEU_bledy)
# wykres_dop(czas, GDOP, PDOP, TDOP, HDOP, VDOP)


# def window():
#     app = QApplication(sys.argv)
#     win = QMainWindow()
#     win.setGeometry(200, 200, 300, 300)
#     win.setWindowTitle("SPP")

#     win.show()
#     sys.exit(app.exec_())

# window()