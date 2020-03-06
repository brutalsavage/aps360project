import manga109api
from PIL import Image, ImageDraw
import numpy as np
import os


# Calculate pixel accuracy for a single image prediction
def pixel_accuracy(prediction=None, labeled=None):


    return 0


# Predict the image mask of the manga input
def predict_sb(input):


    return 0


cleaned_path = "../data cleaning/cleaned mangas/"
label_path = "../data cleaning/manga masks/"

list_of_mangas = os.listdir(cleaned_path)

for mangas in list_of_mangas:
    list_of_images = os.listdir(cleaned_path+mangas+"/")
    for image_name in list_of_images:
        input_image = Image.open(cleaned_path+mangas+"/"+image_name)
        label_image = Image.open(label_path+mangas+"/"+image_name)

        input = np.array(input_image)
        label = np.array(label_image)

        prediction = predict_sb(input)
        pixel_accuracy(prediction=prediction, labeled=label)



