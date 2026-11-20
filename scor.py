from culori import CULORI
from tabla import coordonate_celule

COORD = [tuple(int(v) for v in c) for c in coordonate_celule()]
DIRECTII = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]
SIMBOLURI = {(0, -5): 'R', (5, -5): 'G', (5, 0): 'B', (0, 5): 'O', (-5, 5): 'Y', (-5, 0): 'P'}
ORDINE_SCOR = 'RGOBYP'


def calc_scor(piesa_noua, culoare):
    (celula1, culoare1), (celula2, culoare2) = piesa_noua
    celula1, celula2 = COORD[celula1], COORD[celula2]

    scor = {c: 0 for c in CULORI}
    visited = {celula1, celula2}

    for dq, dr in DIRECTII:
        q, r = celula1[0] + dq, celula1[1] + dr
        while (q, r) not in visited and culoare.get((q, r)) == culoare1:
            scor[culoare1] += 1
            q, r = q + dq, r + dr

        q, r = celula2[0] + dq, celula2[1] + dr
        while (q, r) not in visited and culoare.get((q, r)) == culoare2:
            scor[culoare2] += 1
            q, r = q + dq, r + dr

    return scor


def formateaza_scor(scor):
    return ' '.join(f'{scor[c]}{c}' for c in ORDINE_SCOR if scor[c]) or '-'
