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
