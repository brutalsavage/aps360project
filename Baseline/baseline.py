import manga109api
from PIL import Image, ImageDraw
import numpy as np
import os


# Calculate pixel accuracy for a single image prediction
def pixel_accuracy(prediction=None, labeled=None):

    total_pixels = np.where(labeled == 255)[0].size
    if total_pixels == 0:
        return 1
    count = np.where((prediction==255) & (labeled==255))[0].size
    acc = count/total_pixels

    return acc


# Predict the image mask of the manga input
def predict_sb(input):

    pd = label = np.zeros((1170, 827))

    # Force it to be between [0, 1]
    input = input/255

    #x, y = 0, 0
    kernal_x, kernal_y = 60, 60
    total_pixels = kernal_x*kernal_y
    for x in range(0, 827, kernal_x):
        for y in range(0, 1170, kernal_y):
            temp = input[y:y+kernal_y, x:x+kernal_x]

            white_pixels = np.where(temp>=0.8)[0].size/total_pixels
            black_pixels = np.where(temp<=0.2)[0].size/total_pixels

            if white_pixels > 0.2 and black_pixels > 0.2:
                pd[y:y+kernal_y, x:x+kernal_x] = 255

    return pd


cleaned_path = "../data cleaning/cleaned mangas/"
label_path = "../data cleaning/manga masks/"

list_of_mangas = os.listdir(cleaned_path)
k = 0
for mangas in list_of_mangas:
    list_of_images = os.listdir(cleaned_path+mangas+"/")
    for image_name in list_of_images:
        input_image = Image.open(cleaned_path+mangas+"/"+image_name)
        label_image = Image.open(label_path+mangas+"/"+image_name)

        input = np.array(input_image)
        label = np.array(label_image)

        prediction = predict_sb(input)

        accuracy = pixel_accuracy(prediction=prediction, labeled=label)
        print(accuracy)


