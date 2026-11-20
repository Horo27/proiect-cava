import argparse
import os

import cv2 as cv
import numpy as np

from culori import clasifica_culoare, decupeaza_piesa
from piese import piese_noi_absolut
from scor import COORD, SIMBOLURI, calc_scor, formateaza_scor
from tabla import calculeaza_celule, extrage_careu

TABLA_GOALA = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'CAVA-2026-TEMA1', 'imagini_auxiliare', 'tabla_joc_1.jpg')


def ocupate_din_culoare(culoare):
    return np.array([c in culoare for c in COORD])


def proceseaza_joc(director_joc, joc, celule, director_iesire):
    culoare = dict(SIMBOLURI)
    for i in range(1, 21):
        nume = f'{joc}_{i:02d}'
        tabla = extrage_careu(cv.imread(os.path.join(director_joc, nume + '.jpg')))

        (a, b), _ = piese_noi_absolut(tabla, ocupate_din_culoare(culoare), celule)
        piesa = [(k, clasifica_culoare(decupeaza_piesa(tabla, celule[k]))) for k in (a, b)]
        scor = formateaza_scor(calc_scor(piesa, culoare))

        for k, c in piesa:
            culoare[COORD[k]] = c

        with open(os.path.join(director_iesire, nume + '.txt'), 'w') as f:
            f.write(''.join(f'{k + 1} {c}\n' for k, c in piesa) + scor)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="director cu table-joc/ si table-scor/")
    parser.add_argument("--output", required=True, help="director unde se scriu fisierele .txt")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    celule = calculeaza_celule(extrage_careu(cv.imread(TABLA_GOALA)))

    director_joc = os.path.join(args.input, 'table-joc')
    jocuri = sorted(int(n.split('_')[0]) for n in os.listdir(director_joc) if n.endswith('_01.jpg'))
    for joc in jocuri:
        proceseaza_joc(director_joc, joc, celule, args.output)


if __name__ == "__main__":
    main()
