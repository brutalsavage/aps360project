import torch
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
from PIL import Image
from modelRes import *
import cv2

model = AYAYA_res()
model.load_state_dict(torch.load("../resnet50_bn.pt", map_location=torch.device('cpu')))
model.eval()

data_transforms = transforms.Compose([
        transforms.Resize((448,320)),
        transforms.ToTensor()
        ])

image = Image.open("../Final Image Processing/aaaa.jpg").convert("L").convert('RGB')
image = data_transforms(image).unsqueeze(0)
test_image = image.numpy()
print(image.shape)
out = model(image)
mask = torch.sigmoid(out)

mask_image = torch.Tensor.cpu(mask).detach().numpy() # convert images to numpy for display

f, axarr = plt.subplots(1,2,figsize=(15,15))
axarr[1].imshow(mask_image[0][0])
axarr[0].imshow(cv2.cvtColor(test_image[0][0], cv2.COLOR_RGB2BGR))
plt.show()
