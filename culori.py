import cv2 as cv
import numpy as np

CULORI = 'BGOPRY'
H = 24
RAZA_DISC = 15
PRAG_S = 60
PRAG_V = 60
DEPLASARE_HUE = 20

REFERINTE = {'B': 125.0, 'G': 75.0, 'O': 36.0, 'P': 165.5, 'R': 15.0, 'Y': 51.0}

_yy, _xx = np.mgrid[:2 * H, :2 * H]
DISC = (_xx - H) ** 2 + (_yy - H) ** 2 <= RAZA_DISC ** 2


def decupeaza_piesa(tabla, centru):
    x, y = np.round(centru).astype(int)
    return tabla[y - H:y + H, x - H:x + H]


def masca_simbol(piesa):
    hsv = cv.cvtColor(piesa, cv.COLOR_BGR2HSV)
    return DISC & (hsv[:, :, 1] > PRAG_S) & (hsv[:, :, 2] > PRAG_V), hsv


def hue_piesa(piesa):
    masca, hsv = masca_simbol(piesa)
    return np.median((hsv[:, :, 0][masca].astype(int) + DEPLASARE_HUE) % 180)


def antreneaza_hue(piese, etichete):
    hue = np.array([hue_piesa(p) for p in piese])
    return {c: float(np.median(hue[etichete == c])) for c in CULORI}


def clasifica_culoare(piesa, referinte=REFERINTE):
    h = hue_piesa(piesa)
    return min(referinte, key=lambda c: abs(h - referinte[c]))
