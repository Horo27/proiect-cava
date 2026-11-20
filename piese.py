import cv2 as cv
import numpy as np

from culori import DISC, decupeaza_piesa
from tabla import perechi_vecine

PRAG_V_OCUPAT = 220
PERECHI = perechi_vecine()


def luminozitate_celule(tabla, celule):
    v = cv.cvtColor(tabla, cv.COLOR_BGR2HSV)[:, :, 2]
    return np.array([decupeaza_piesa(v, c)[DISC].mean() for c in celule])


def celule_ocupate(tabla, celule, prag=PRAG_V_OCUPAT):
    return luminozitate_celule(tabla, celule) < prag


def piese_noi_absolut(tabla, ocupate_anterior, celule):
    v = luminozitate_celule(tabla, celule)
    i, j = PERECHI.T
    scor = v[i] + v[j]
    scor[ocupate_anterior[i] | ocupate_anterior[j]] = np.inf
    return PERECHI[np.argmin(scor)], scor


def schimbare_celule(tabla, anterioara, celule):
    dif = cv.absdiff(tabla, anterioara).max(axis=2)
    return np.array([decupeaza_piesa(dif, c)[DISC].mean() for c in celule])


def piese_noi_diferenta(tabla, anterioara, celule):
    d = schimbare_celule(tabla, anterioara, celule)
    i, j = PERECHI.T
    scor = d[i] + d[j]
    return PERECHI[np.argmax(scor)], scor
