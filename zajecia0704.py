from readrnx_studenci import *
from utils import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
import sys

class MyWindow(QMainWindow):
    
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(100, 90, 700, 900)
        self.setWindowTitle("SNS - ćwiczenie 2: SPP")
        self.initUI()

    def initUI(self):
        self.btnObs()
        self.txtEditObs()
        self.btnNav()
        self.txtEditNav()

        self.labelStart()
        self.txtEditStartYear()
        self.txtEditStartMonth()
        self.txtEditStartDay()
        self.txtEditStartHour()
        self.txtEditStartMinute()
        self.txtEditStartSecond()
        
        self.labelKoniec()
        self.txtEditKoniecYear()
        self.txtEditKoniecMonth()
        self.txtEditKoniecDay()
        self.txtEditKoniecHour()
        self.txtEditKoniecMinute()
        self.txtEditKoniecSecond()

        self.labelMaska()
        self.txtEditMaska()

        self.btnUruchom()

        self.btnWykresBlXYZ()
        self.btnWykresBlNEU()
        self.btnWykresLSats()
        self.btnWykresPunktowyNE()
        self.btnWykresDOP()
        self.btnWyswietlFolderZWynikami()

    def btnObs(self):
        self.btnObs = QtWidgets.QPushButton("Wybór pliku obserwacyjnego", self)
        self.btnObs.setGeometry(10, 10, 200, 40)
        self.btnObs.clicked.connect(self.btnObsClick)

    def txtEditObs(self):
        self.txtEditObs = QtWidgets.QTextEdit("./kod/obs.rnx", self)
        self.txtEditObs.setGeometry(220, 10, 470, 40)
        self.txtEditObs.setReadOnly(True)

    def btnObsClick(self):
        self.fileName = QFileDialog.getOpenFileName(self, "Wybierz plik obserwacyjny", "/home/", "")
        self.txtEditObs.setText(self.fileName[0])

    def btnNav(self):
        self.btnNav = QtWidgets.QPushButton("Wybór pliku nawigacyjnego", self)
        self.btnNav.setGeometry(10, 60, 200, 40)
        self.btnNav.clicked.connect(self.btnNavClick)

    def txtEditNav(self):
        self.txtEditNav = QtWidgets.QTextEdit("./kod/nav.rnx", self)
        self.txtEditNav.setGeometry(220, 60, 470, 40)
        self.txtEditNav.setReadOnly(True)

    def btnNavClick(self):
        self.fileName = QFileDialog.getOpenFileName(self, "Wybierz plik nawigacyjny", "/home/", "")
        self.txtEditNav.setText(self.fileName[0])

    def labelStart(self):
        self.labelStart = QtWidgets.QLabel("Start pomiaru:", self)
        self.labelStart.setGeometry(10, 120, 106, 40)
        
    startX = 125
    def txtEditStartYear(self):
        self.txtEditStartYear = QtWidgets.QTextEdit(self)
        self.txtEditStartYear.setGeometry(self.startX, 120, 86, 40)
        self.txtEditStartYear.setText("2022")

    def txtEditStartMonth(self):
        self.txtEditStartMonth = QtWidgets.QTextEdit(self)
        self.txtEditStartMonth.setGeometry(self.startX + 95, 120, 86, 40)
        self.txtEditStartMonth.setText("3")

    def txtEditStartDay(self):
        self.txtEditStartDay = QtWidgets.QTextEdit(self)
        self.txtEditStartDay.setGeometry(self.startX + 2*96, 120, 86, 40)
        self.txtEditStartDay.setText("21")

    def txtEditStartHour(self):
        self.txtEditStartHour = QtWidgets.QTextEdit(self)
        self.txtEditStartHour.setGeometry(self.startX + 3*96, 120, 86, 40)
        self.txtEditStartHour.setText("0")
        
    def txtEditStartMinute(self):
        self.txtEditStartMinute = QtWidgets.QTextEdit(self)
        self.txtEditStartMinute.setGeometry(self.startX + 4*96, 120, 86, 40)
        self.txtEditStartMinute.setText("0")

    def txtEditStartSecond(self):
        self.txtEditStartSecond = QtWidgets.QTextEdit(self)
        self.txtEditStartSecond.setGeometry(self.startX + 5*96, 120, 86, 40)
        self.txtEditStartSecond.setText("0")

    def labelKoniec(self):
        self.labelKoniec = QtWidgets.QLabel("Koniec pomiaru:", self)
        self.labelKoniec.setGeometry(10, 170, 106, 40)
        
    def txtEditKoniecYear(self):
        self.txtEditKoniecYear = QtWidgets.QTextEdit(self)
        self.txtEditKoniecYear.setGeometry(self.startX, 170, 86, 40)
        self.txtEditKoniecYear.setText("2022")

    def txtEditKoniecMonth(self):
        self.txtEditKoniecMonth = QtWidgets.QTextEdit(self)
        self.txtEditKoniecMonth.setGeometry(self.startX + 95, 170, 86, 40)
        self.txtEditKoniecMonth.setText("3")

    def txtEditKoniecDay(self):
        self.txtEditKoniecDay = QtWidgets.QTextEdit(self)
        self.txtEditKoniecDay.setGeometry(self.startX + 2*96, 170, 86, 40)
        self.txtEditKoniecDay.setText("21")

    def txtEditKoniecHour(self):
        self.txtEditKoniecHour = QtWidgets.QTextEdit(self)
        self.txtEditKoniecHour.setGeometry(self.startX + 3*96, 170, 86, 40)
        self.txtEditKoniecHour.setText("0")
        
    def txtEditKoniecMinute(self):
        self.txtEditKoniecMinute = QtWidgets.QTextEdit(self)
        self.txtEditKoniecMinute.setGeometry(self.startX + 4*96, 170, 86, 40)
        self.txtEditKoniecMinute.setText("30")

    def txtEditKoniecSecond(self):
        self.txtEditKoniecSecond = QtWidgets.QTextEdit(self)
        self.txtEditKoniecSecond.setGeometry(self.startX + 5*96, 170, 86, 40)
        self.txtEditKoniecSecond.setText("0")

    def labelMaska(self):
        self.labelMaska = QtWidgets.QLabel("Maska pomiaru:", self)
        self.labelMaska.setGeometry(10, 220, 106, 40)

    def txtEditMaska(self):
        self.txtEditMaska = QtWidgets.QTextEdit(self)
        self.txtEditMaska.setGeometry(self.startX + 5*96, 220, 86, 40)
        self.txtEditMaska.setText("10")

    def btnUruchom(self):
        self.btnUruchom = QtWidgets.QPushButton("Uruchom", self)
        self.btnUruchom.setGeometry(10, 280, 680, 40)
        self.btnUruchom.clicked.connect(self.btnUruchomClick)

        # 320 + 20

    def btnUruchomClick(self):
        nav_file = self.txtEditNav.toPlainText()
        obs_file = self.txtEditObs.toPlainText()

        rok_start = int(self.txtEditStartYear.toPlainText())
        miesiac_start = int(self.txtEditStartMonth.toPlainText())
        dzien_start = int(self.txtEditStartDay.toPlainText())
        godzina_start = int(self.txtEditStartHour.toPlainText())
        minuta_start = int(self.txtEditStartMinute.toPlainText())
        sekunda_start = int(self.txtEditStartSecond.toPlainText())

        rok_koniec = int(self.txtEditKoniecYear.toPlainText())
        miesiac_koniec = int(self.txtEditKoniecMonth.toPlainText())
        dzien_koniec = int(self.txtEditKoniecDay.toPlainText())
        godzina_koniec = int(self.txtEditKoniecHour.toPlainText())
        minuta_koniec = int(self.txtEditKoniecMinute.toPlainText())
        sekunda_koniec = int(self.txtEditKoniecSecond.toPlainText())

        time_start =  [rok_start, miesiac_start, dzien_start, godzina_start, minuta_start, sekunda_start]
        time_end =    [rok_koniec, miesiac_koniec, dzien_koniec, godzina_koniec, minuta_koniec, sekunda_koniec]

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

        self.XYZ_obl, self.czas, self.l_sats, self.GDOP, self.PDOP, self.TDOP, self.HDOP, self.VDOP = wsp_popr(tow, tow_end, inav, nav, alfa, beta, dt, obs, iobs, XYZ_ref, u, we, c, maska)
        self.XYZ_bledy, self.NEU_bledy = bledy_wsp(XYZ_ref, self.XYZ_obl)
        np.savetxt('./wyniki/XYZ_wyniki.txt', self.XYZ_obl, delimiter=', ', fmt='%1.8f')
        np.savetxt('./wyniki/XYZ_bledy.txt', self.XYZ_bledy, delimiter=', ', fmt='%1.8f')
        np.savetxt('./wyniki/NEU_bledy.txt', self.NEU_bledy, delimiter=', ', fmt='%1.8f')

        self.mean, self.std_dev, mean_square_err, min_val, max_val = analiza_bledow(self.XYZ_bledy)
        self.mean_neu, self.std_dev_neu, mean_square_err_neu, min_val_neu, max_val_neu = analiza_bledow(self.NEU_bledy)

        print(self.mean_neu)

    def btnWykresBlXYZ(self):
        self.btnWykresBlXYZ = QtWidgets.QPushButton("Wykresy liniowe wartości poszczególnych błędów współrzędnych XYZ", self)
        self.btnWykresBlXYZ.setGeometry(10, 600, 680, 40)
        self.btnWykresBlXYZ.clicked.connect(self.btnWykresBlXYZClick)

    def btnWykresBlXYZClick(self):
        wykres_bledow(self.czas, self.XYZ_bledy, "xyz", self.mean, self.mean_neu, self.std_dev, self.std_dev_neu)

    def btnWykresBlNEU(self):
        self.btnWykresBlNEU = QtWidgets.QPushButton("Wykresy liniowe wartości poszczególnych błędów współrzędnych NEU", self)
        self.btnWykresBlNEU.setGeometry(10, 650, 680, 40)
        self.btnWykresBlNEU.clicked.connect(self.btnWykresBlNEUClick)

    def btnWykresBlNEUClick(self):
        wykres_bledow(self.czas, self.XYZ_bledy, "neu", self.mean, self.mean_neu, self.std_dev, self.std_dev_neu)

    def btnWykresLSats(self):
        self.btnWykresLSats = QtWidgets.QPushButton("Wykres liczby satelitów", self)
        self.btnWykresLSats.setGeometry(10, 700, 680, 40)
        self.btnWykresLSats.clicked.connect(self.btnWykresLSatsClick)

    def btnWykresLSatsClick(self):
        wykres_l_sats(self.czas, self.l_sats)

    def btnWykresPunktowyNE(self):
        self.btnWykresPunktowyNE = QtWidgets.QPushButton("Wykres punktowy błędów współrzędnych płaskich n i e", self)
        self.btnWykresPunktowyNE.setGeometry(10, 750, 680, 40)
        self.btnWykresPunktowyNE.clicked.connect(self.btnWykresPunktowyNEClick)

    def btnWykresPunktowyNEClick(self):
        wykres_punktowy_n_e(self.NEU_bledy)

    def btnWykresDOP(self):
        self.btnWykresDOP = QtWidgets.QPushButton("Wykres współczynników DOP", self)
        self.btnWykresDOP.setGeometry(10, 800, 680, 40)
        self.btnWykresDOP.clicked.connect(self.btnWykresDOPClick)

    def btnWykresDOPClick(self):
        wykres_dop(self.czas, self.GDOP, self.PDOP, self.TDOP, self.HDOP, self.VDOP)

    def btnWyswietlFolderZWynikami(self):
        self.btnWyswietlFolderZWynikami = QtWidgets.QPushButton("Otwórz folder w wynikami zapisanymi w plikach tekstowych", self)
        self.btnWyswietlFolderZWynikami.setGeometry(10, 850, 680, 40)
        # self.btnWykresDOP.clicked.connect(self.btnWykresDOPClick)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

# nav_file = './kod/nav.rnx'
# obs_file = './kod/obs.rnx'

# time_start =  [2022, 3, 21, 0, 0, 0]
# time_end =    [2022, 3, 21, 20, 10, 0]

# nav, inav = readrnxnav(nav_file)
# obs, iobs = readrnxobs(obs_file, time_start, time_end, 'G')

# # stale
# maska = 10
# u = 3.986005 * pow(10, 14)
# we = 7.2921151467 * pow(10, -5)
# c = 299792458.0
# dt = 30
# alfa, beta = alfa_beta(nav_file)

# XYZ_ref = wsp_odbiornika(obs_file)
# nav, inav, obs, iobs = porzadek(nav, inav, obs, iobs)

# week, tow = date2tow(time_start)[0:2]
# week_end, tow_end = date2tow(time_end)[0:2]

# XYZ_obl, czas, l_sats, GDOP, PDOP, TDOP, HDOP, VDOP = wsp_popr(tow, tow_end, inav, nav, alfa, beta, dt, obs, iobs, XYZ_ref, u, we, c, maska)
# XYZ_bledy, NEU_bledy = bledy_wsp(XYZ_ref, XYZ_obl)
# np.savetxt('./wyniki/test.txt', XYZ_bledy, delimiter=', ', fmt='%1.8f')

# mean, std_dev, mean_square_err, min_val, max_val = analiza_bledow(XYZ_bledy)
# mean_neu, std_dev_neu, mean_square_err_neu, min_val_neu, max_val_neu = analiza_bledow(NEU_bledy)

# wykres_bledow(czas, XYZ_bledy, "xyz", mean, mean_neu, std_dev, std_dev_neu)
# # wykres_bledow(czas, NEU_bledy, "neu", mean, mean_neu, std_dev, std_dev_neu)
# # wykres_l_sats(czas, l_sats)
# # wykres_punktowy_n_e(NEU_bledy)
# # wykres_dop(czas, GDOP, PDOP, TDOP, HDOP, VDOP)
