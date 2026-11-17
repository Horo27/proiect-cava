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


def deseneaza_puncte(image, puncte, title, etichete=False):
    vis = image.copy()
    for i, (x, y) in enumerate(puncte):
        cv.circle(vis, (int(x), int(y)), 5, (0, 0, 255), -1)
        if etichete:
            cv.putText(vis, str(i + 1), (int(x) - 10, int(y) - 7), cv.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
    show_image(vis, title, size=(10, 10))
