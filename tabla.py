import cv2 as cv
import numpy as np

from utils import show_image


def extrage_careu(image, debug=False):
    image_blur = cv.medianBlur(image, 5)
    image_hsv = cv.cvtColor(image_blur, cv.COLOR_BGR2HSV)
    if debug: show_image(image_hsv[:, :, 0], 'canal Hue')

    thresh = cv.inRange(image_hsv, (60, 0, 0), (140, 255, 255))

    kernel = np.ones((15, 15), np.uint8)
    thresh = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel)
    if debug: show_image(thresh, 'image_thresholded')

    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    max_area = 0

    for i in range(len(contours)):
        if(len(contours[i]) >3):
            possible_top_left = None
            possible_bottom_right = None
            for point in contours[i].squeeze():
                if possible_top_left is None or point[0] + point[1] < possible_top_left[0] + possible_top_left[1]:
                    possible_top_left = point

                if possible_bottom_right is None or point[0] + point[1] > possible_bottom_right[0] + possible_bottom_right[1] :
                    possible_bottom_right = point

            diff = np.diff(contours[i].squeeze(), axis = 1)
            possible_top_right = contours[i].squeeze()[np.argmin(diff)]
            possible_bottom_left = contours[i].squeeze()[np.argmax(diff)]
            if cv.contourArea(np.array([[possible_top_left],[possible_top_right],[possible_bottom_right],[possible_bottom_left]])) > max_area:
                max_area = cv.contourArea(np.array([[possible_top_left],[possible_top_right],[possible_bottom_right],[possible_bottom_left]]))
                top_left = possible_top_left
                bottom_right = possible_bottom_right
                top_right = possible_top_right
                bottom_left = possible_bottom_left

    width = 810
    height = 810

    if debug:
        image_copy = image.copy()
        for p in [top_left, top_right, bottom_right, bottom_left]:
            cv.circle(image_copy, tuple(int(v) for v in p), 40, (0, 0, 255), -1)
        show_image(image_copy, 'detected corners')

    puzzle = np.array([top_left,top_right,bottom_right,bottom_left], dtype = "float32")
    destination_of_puzzle = np.array([[0,0],[width,0],[width,height],[0,height]], dtype = "float32")

    M = cv.getPerspectiveTransform(puzzle,destination_of_puzzle)
    result = cv.warpPerspective(image, M, (width, height))

    return result


def detecteaza_template(gray, centru_template, prag=0.4, debug=False):
    cx, cy = centru_template
    h = 26
    template = gray[cy - h:cy + h, cx - h:cx + h]
    if debug:
        show_image(template, 'template', size=(3, 3))

    corr = cv.matchTemplate(gray, template, cv.TM_CCOEFF_NORMED)
    if debug:
        show_image(corr, 'harta de corelatie')

    maxim_local = corr == cv.dilate(corr, np.ones((25, 25), np.uint8))
    ys, xs = np.where(maxim_local & (corr > prag))
    return np.stack([xs + h, ys + h], axis=1).astype(float)


def potriveste_grila(puncte, cx=405, cy=403, dx=42.3, prag_eroare=8):
    for _ in range(5):
        dy = dx * np.sqrt(3) / 2
        r = np.round((puncte[:, 1] - cy) / dy)
        q = np.round((puncte[:, 0] - cx) / dx - r / 2)
        eroare = np.hypot(puncte[:, 0] - (cx + dx * (q + r / 2)), puncte[:, 1] - (cy + dy * r))
        bune = eroare < prag_eroare

        n = bune.sum()
        A = np.zeros((2 * n, 3))
        b = np.zeros(2 * n)
        A[0::2, 0] = 1
        A[0::2, 2] = (q + r / 2)[bune]
        b[0::2] = puncte[bune, 0]
        A[1::2, 1] = 1
        A[1::2, 2] = (np.sqrt(3) / 2 * r)[bune]
        b[1::2] = puncte[bune, 1]
        cx, cy, dx = np.linalg.lstsq(A, b, rcond=None)[0]
    return (cx, cy, dx), bune, eroare


def genereaza_celule(cx, cy, dx):
    dy = dx * np.sqrt(3) / 2
    celule = []
    for r in range(-5, 6):
        for q in range(-5, 6):
            s = -q - r
            if max(abs(q), abs(r), abs(s)) > 5:
                continue
            if sorted([abs(q), abs(r), abs(s)]) == [0, 5, 5]:
                continue
            celule.append((cx + dx * (q + r / 2), cy + dy * r))
    return np.array(celule)


def calculeaza_celule(tabla_goala, centru_template=(341, 291), debug=False):
    gray = cv.cvtColor(tabla_goala, cv.COLOR_BGR2GRAY)
    puncte = detecteaza_template(gray, centru_template, debug=debug)
    parametri, _, _ = potriveste_grila(puncte)
    return genereaza_celule(*parametri)
