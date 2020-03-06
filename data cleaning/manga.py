import manga109api
from pprint import pprint
from PIL import Image, ImageDraw
import numpy as np
import os.path
import json
import gc

def draw_rectangle(img, x0, y0, x1, y1, annotation_type):
    assert annotation_type in ["body", "face", "frame", "text"]
    color = {"body": "#258039", "face": "#f5be41",
             "frame": "#31a9b8", "text": "#cf3721"}[annotation_type]
    width = 10
    draw = ImageDraw.Draw(img)
    draw.line([x0 - width/2, y0, x1 + width/2, y0], fill=color, width=width)
    draw.line([x1, y0, x1, y1], fill=color, width=width)
    draw.line([x1 + width/2, y1, x0 - width/2, y1], fill=color, width=width)
    draw.line([x0, y1, x0, y0], fill=color, width=width)


manga109_root_dir  = "C:/Users/Steven Xia/Desktop/Manga109/Manga109_2017_09_28"
p = manga109api.Parser(root_dir=manga109_root_dir)

books = p.books[0:2]

for book_title in books:

    filepath = "cleaned mangas/"+book_title
    labelpath = "manga masks/"+book_title

    # Safety step
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    if not os.path.exists(labelpath):
        os.mkdir(labelpath)

    filepath+= "/"
    labelpath+= "/"

    for index in range(len(p.annotations[book_title]["book"]["pages"]["page"])):
        #print(index)
        # what is the file name smile
        filename = book_title+"_page_"+str(index) + "_"

        # open original image
        img = Image.open(p.img_path(book=book_title, index=index))

        # one half and the other half
        one_half = img.crop((0,0,827,1170))
        one_half = one_half.convert("L")
        second_half = img.crop((827,0, 1654, 1170))
        second_half = second_half.convert("L")
        one_half.save(filepath+filename+"1.jpg")
        second_half.save(filepath+filename+"2.jpg")

        # adjusting the label
        label = np.zeros((1170, 1654))
        if "text" in p.annotations[book_title]["book"]["pages"]["page"][index]:
            rois = p.annotations[book_title]["book"]["pages"]["page"][index]["text"]

            # This api is pretty bad
            if not isinstance(rois, list):
                rois = [rois]

            for roi in rois:
                x_1 = roi["@xmin"]
                x_2 = roi["@xmax"]
                y_1 = roi["@ymin"]
                y_2 = roi["@ymax"]
                label[y_1:y_2, x_1:x_2] = 1.0

        label_1 = label[:, 0:827]*255
        label_2 = label[:, 827:]*255

        label1 = Image.fromarray(label_1)
        label2 = Image.fromarray(label_2)

        label1 = label1.convert("L")
        label2 = label2.convert("L")

        label1.save(labelpath+filename+"1.jpg")
        label2.save(labelpath+filename+"2.jpg")

