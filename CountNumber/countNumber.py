import os

import cv2
from ultralytics import YOLO

model_path = '../runs/wheat/train/weights/best.pt'
image_source_file = 'D:/B_Dataset/global-wheat-detection/test'
model = YOLO(model_path)
# load the image from the file
images = []
img_names = []
for image in os.listdir(image_source_file):
    img_names.append(image)
    image = os.path.join(image_source_file, image)
    img = cv2.imread(image)
    images.append(img)

results = model(images, stream=True)
# process the results generator
i = 0
for result in results:
    img = result.plot()
    count = len(result.boxes.xywh)
    cv2.putText(img, f"Count : {count}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
    #     save the image with original name
    cv2.imwrite(img_names[i], img)
    i += 1
