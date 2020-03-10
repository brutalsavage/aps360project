import manga109api
from PIL import Image, ImageDraw
import numpy as np
import os
import statistics

# Calculate pixel accuracy for a single image prediction
def pixel_accuracy(prediction=None, labeled=None):

    # intersection/union-intersection

    intersection = np.where((prediction==255) & (labeled==255))[0].size
    #intersection = np.count_nonzero((prediction==255) & (labeled==255))
    union = np.where((prediction==255))[0].size+np.where((labeled==255))[0].size - intersection
    acc = intersection/union
    #print(acc)
    return acc



kernal_inside = np.zeros((40,40))
kernal_inside[25:35, 25:35] = 1
kernal_outside = np.zeros((40,40))
kernal_outside = kernal_outside+1
kernal_outside[25:35, 25:35] = 0

# Predict the image mask of the manga input
def predict_sb(input):

    pd = label = np.zeros((448, 320))

    # Force it to be between [0, 1]
    input = input/255
    ones = input > 0.6
    input[ones] = 1
    zeros = input < 0.4
    input[zeros] = 0

    kernal_x, kernal_y = 40, 40
    total_pixels = kernal_x*kernal_y
    for x in range(0, 320-40, 10):
        for y in range(0, 448-40,10):

            temp = input[y:y+kernal_y, x:x+kernal_x]
            outside = np.multiply(temp, kernal_outside)
            inside = np.multiply(temp, kernal_inside)

            inside_pixels = np.where(inside==0)[0].size/(10*10)
            outside_pixels = np.where(outside==1)[0].size/total_pixels

            if outside_pixels > 0.8 and inside_pixels > 0.8:
                pd[y:y+kernal_y, x:x+kernal_x] = 255

    return pd


cleaned_path = "../data cleaning/small mangas/"
label_path = "../data cleaning/small masks/"

list_of_mangas = os.listdir(cleaned_path)[0:2]
k = 0

hist_accuracy = []

for mangas in list_of_mangas:
    list_of_images = os.listdir(cleaned_path+mangas+"/")
    for image_name in list_of_images:
        input_image = Image.open(cleaned_path+mangas+"/"+image_name)
        label_image = Image.open(label_path+mangas+"/"+image_name)

        input = np.array(input_image)
        label = np.array(label_image)

        prediction = predict_sb(input)
        # label1 = Image.fromarray(prediction)
        # label1.show()
        #
        # label2 = Image.fromarray(label)
        # label2.show()
        #exit()
        accuracy = pixel_accuracy(prediction=prediction, labeled=label)
        print(accuracy)
        hist_accuracy.append(accuracy)

print(statistics.mean(hist_accuracy))
print(max(hist_accuracy))


