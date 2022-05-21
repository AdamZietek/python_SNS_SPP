# -*- coding: utf-8 -*-
"""

@author: Maciek


"""
import numpy as np
from readrnx_studenci import readrnxnav, readrnxobs, date2tow

# cieżka do pliku nawigacyjnego
nav_file = 'WROC00POL_R_20220800000_01D_GN.rnx'
# cieżka do pliku obserwacyjnego
obs_file = 'WROC00POL_R_20220800000_01D_30S_MO.rnx'

# zdefiniowanie czasu obserwacji: daty początkowej i końcowej
# dla pierwszej epoki z pliku będzie to:
time_start =  [2022, 3, 21, 0, 0, 0]  
time_end =    [2022, 3, 21, 0, 0, 0] 

# odczytanie danych z pliku obserwacyjnego
obs, iobs = readrnxobs(obs_file, time_start, time_end, 'G')
# odczytanie danych z pliku nawigacyjnego:
nav, inav = readrnxnav(nav_file)
# filtrowanie danych: satelity "unhealthy"


#%%
"""
zdefiniowanie współrzędnych przybliżonych odbiornika - mogą to być współrzędne z nagłówka 
pliku obserwacyjnego, skopiowane "z palca" lub pobierane automatycznie z treci nagłówka
"""

"""
Wprowadzenie ustawień, takich jak maska obserwacji, czy typ poprawki troposferycznej
"""
el_mask = 0 # elevation mask/cut off in degrees

"""
Przeliczenie daty początkowej i końcowej do sekund tygodnia GPS - niezbędne w celu
poprawnej definicji pętli związanej z czasem obserwacji w ciągu całej doby
"""
week, tow = date2tow(time_start)[0:2]
week_end, tow_end = date2tow(time_end)[0:2]
#%% Obliczenia

"""
Otwieramy dużą pętlę
for t in range(tow, tow_end+1, dt): gdzie dt równe 30
    Wewnątrz tej pętli, zajmujemy się obserwacjami wyłącznie dla jednej epoki (epoka t), zatem:
        1. Wybieramy obserwacje dla danej epoki, na podstawie tablicy iobs oraz naszej epoki t
        czyli, wybieramy te obserwacje z tablicy obs, dla których w tablicy iobs ostatnia kolumna 
        jest równa t - zmienna Pobs
        2. wybieramy satelity, obserwowane w danej epoce, na podstawie tablicy iobs - na podstawie 
        naszego t - zmienna sats
        3. Definiujemy wartosci przybliżone: współrzędne odbiornika xr oraz błąd zegara odbiornika
        dtr = 0 oraz czasu propagacji sygnału tau = 0.072
        4. Najprawdopodobniej przyda się definicja pustych wektorów, np. zawierających 
        odległosci geometryczne (wartoci przybliżone na podstawie tau) lub 
        
    Przechodzimy do iteracyjnych obliczeń współrzędnych odbiornika:
        pętla for (lub while), do testowania programu przyjmujemy pętle for dla 5 iteracji
        Po weryfikacji działania programu, można zamienić pętlę for na pętle while, dopisując
        warunek zbieżnoci kolejnych współrzędnych - skróci nam to czas obliczeń, ponieważ w 
        praktyce nie potrzeba jest nam 5 iteracji, ale najczęciej 3
        
        for i in range(5):
            Wykonujemy kolejne obliczenia, niezależnie dla kolejnych satelitów, obserwowanych
            w danej epoce, czyli pr*zechodzimy do pętli:
                for sat in sats: (przyda nam się tutaj również indeks satelity, więc byłoby
                                  to co np. for i, sat in enumerate(sats):)
                    Obliczamy czas emisji sygnału:
                        tr = t - tau + dtr
                    Kolejne kroki, znane z poprzedniego ćwiczenia:
                    wyznaczamy współrzędne satelity xs (oraz błąd zegara satelity dts) na czas tr (UWAGA, w kolejnych iteracjach
                    czas tr będzie się zmieniał i aktualizował, neizależnie dla każdego satelity)
                    
                    Odległosć geometryczna:
                        1. rotacja do układu chwilowego - otrzymujemy xs_rot
                        2. Na podstawie xs_rot obliczamy odległosć geometryczną rho
                        
                    Obliczamy elewację i azymut
                    Macierz Rneu definiujemy na podstawie xr, przeliczonego do współrzędnych
                    phi lambda, algorytmem Hirvonena
                    
                    Odrzucamy satelity znajdujące się poniżej maski
                    
                    Obliczamy poprawki atmosferyczne:
                        trop oraz iono
                    
                    Wyznaczamy pseudoodległosć przybliżoną (obliczoną), jako:
                        Pcalc = rho - cdts + dtr + trop + iono
                        
                    Wyznaczamy kolejen elementy wektora wyrazów wolnych y, jako:
                        y = Pcalc - Pobs
                        
                    Budujemy kolejne wiersze macierzy A:
                
                Kończymy pętle dla kolejnych satelitów
                
                1. Łączymy ze sobą elementy wektora wyrazów wolych w jeden wektor
                2. Łączymy ze sobą kolejnę wiersze macierz współczynników A
                3. Rozwiązujemy układ równać, metodą najmniejszych kwadratów
                
                x = -np.linalg.inv(A.T@A) @ (A.T @ y)
                
                gdzie x jest wektorem zawierającym szukane przyrosty do niewiadomych
                
                Aktualizujemy wartosci przybliżone o odpowiednie elementy wektora x
                xr[0] = xr[0] + x[0]
                xr[1] = xr[1] + x[1]
                xr[2] = xr[2] + x[2]
                dtr = dtr + x[3]/c 
                
                Tak obliczone wartoci xr oraz dtr stanowią wartoci wejsciowe do kolejnej iteracji, itd 
                do skończenia piątej iteracji lub spełnienia warunku zbieżnoci współrzędncyh
            
            
            Po skończeniu 5. iteracji, zbieramy obliczone współrzędne xr - warto zebrać również
            liczby obserwowanych satelitów, obliczone wartoci współczynników DOP (przynajmniej PDOP)
            
"""








