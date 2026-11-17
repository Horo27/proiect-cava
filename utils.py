import cv2 as cv
import matplotlib.pyplot as plt


def show_image(image, title='', size=(8, 8)):
    plt.figure(figsize=size)
    if image.ndim == 3:
        plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))
    else:
        plt.imshow(image, cmap='gray')
    plt.title(title)
    plt.axis('off')
    plt.show()
