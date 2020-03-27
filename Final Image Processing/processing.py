import numpy as np
import os
from PIL import Image, ImageDraw
import cv2

def denoise(img, Gaussian=False, Morph=False, th=0.3):

    # Apply Bilateral Filter
    # Reason why bilateral is better is because it keeps sharp edges
    if Gaussian:
        img = cv2.bilateralFilter(img, 20, 200,200)

    # Apply threshold value
    img[img > th * 255] = 255
    img[img <= th * 255] = 0

    # Apply Morphological Opening
    if Morph:
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (3,3)))
    return img

img = cv2.imread("test.jpg", cv2.IMREAD_GRAYSCALE)

img2 = denoise(img, Gaussian=True, Morph=True)
cv2.imshow("test",img2)
cv2.waitKey()