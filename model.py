from ultralytics import YOLO
import numpy as np
from PIL import Image
import os


def detect_with_dir():
    dir = os.getcwd()
    model_dir = r"\runs\detect\train_high_Res\weights\best.pt"
    model = YOLO(model_dir, task="detect") # Loading the YOLO model
    img_dir = "../custom_dataset/test/full\\"
    for img in os.listdir(dir+img_dir):
        if img.endswith(".jpg") or img.endswith(".png"):
            path = dir+img_dir + img

            results = model.predict(path, save=False, conf=0.65)

            for result in results:
                i = 0
                image = Image.open(path)
                cords = np.round(result.boxes.xyxy).astype(int)
                for x in cords:
                    i += 1
                    box = image.crop(x.tolist())
                    # Prevents images too small for classification from being saved
                    if box.size[0] >= 75 and box.size[1] >= 75:
                        # Prevents extremely wide but very short or extremely long but very narrow images from being saved
                        if not box.size[0]*2.5 < box.size[1] and not box.size[1]*2.5 < box.size[0]:
                            box.save("test_result\\"+img[:]+"__"+str(i)+".jpg", verbose=0)

        else:
            print("Wrong format")


def detect_with_image(img):
    dir = os.getcwd()
    model_dir = dir + r"\runs\detect\train_high_Res\weights\best.pt"
    model = YOLO(model_dir, task="detect")
    results = model.predict(img, save=False, conf=0.65)
    images = []
    for result in results:
       
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            if x2-x1 >= 65 and y2-y1 >= 65:
                if (x2-x1) * 2.5 > y2-y1 and (y2-y1) * 2.5 > x2-x1:
                    cropped_object = img.crop((x1, y1, x2, y2))
                    print("x1="+str(x1)+" x2="+str(x2)+" y1="+str(y1)+" y2="+str(y2))
                    images.append(cropped_object)

    return images
