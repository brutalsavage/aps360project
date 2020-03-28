import numpy as np
import os
from PIL import Image
import cv2


def denoise(img, Gaussian=False, Morph=False, th=0.3):

    # Apply Bilateral Filter
    # Reason why bilateral is better is because it keeps sharp edges
    if Gaussian:
        img = cv2.bilateralFilter(img, 20, 200,200)
        #img = cv2.GaussianBlur(img, (37,37),0)

    # Apply threshold value
    img[img > th * 255] = 255
    img[img <= th * 255] = 0

    # Apply Morphological Opening
    if Morph:
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (3,3)))
    return img

def apply_alpha(img, source_img):

    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # find contours with simple approximation
    #print(contours)

    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGBA)
    #img[(img[:,:]==[0,0,0,255]).all()] = [100,100,100,255]

    #cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
    for index in range(len(img)):
        for index_2 in range(len(img[0])):
            if not (img[index, index_2] == [0,0,0,255]).all():
                img[index, index_2] = [255,255,0,255]
            else:
                img[index, index_2] = [0,0,0,0]


    img = cv2.resize(img, (len(source_img[0]),len(source_img)), interpolation=cv2.INTER_NEAREST)
    return img

def adjust(img, source_img):
    img[np.where((img==[0,0,0,0]).all(axis = 2))] = source_img[np.where((img==[0,0,0,0]).all(axis = 2))]
    return img

if __name__ == "__main__":
    img = cv2.imread("test.jpg", cv2.IMREAD_GRAYSCALE)
    img = denoise(img, Gaussian=True, Morph=True, th=0.3)

    source_img = cv2.imread("aaaa.jpg", -1)
    source_img = cv2.cvtColor(source_img, cv2.COLOR_BGRA2RGBA)
    #source_img = source_img[:, 0:827]

    img = apply_alpha(img, source_img)
    img = adjust(img, source_img)

    dst_img = cv2.addWeighted(img, 0.5, source_img, 0.5, 0)
    dst_img_file = Image.fromarray(dst_img, 'RGBA')
    dst_img_file.show()
    #dst_img_file.save("test.png")