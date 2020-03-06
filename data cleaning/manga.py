import manga109api
from pprint import pprint
from PIL import Image, ImageDraw

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

print(len(p.books))
img = Image.open(p.img_path(book="LoveHina_vol01", index=14))
for annotation_type in ["body", "face", "frame", "text"]:
    rois = p.annotations["LoveHina_vol01"]["book"]["pages"]["page"][14][annotation_type]
    for roi in rois:
        draw_rectangle(img, roi["@xmin"], roi["@ymin"], roi["@xmax"], roi["@ymax"], annotation_type)

img.show()