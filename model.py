from ultralytics import YOLO
import torch
from PIL import Image
import os


def detect_with_dir():
    dir = os.getcwd()
    model_dir = r"\runs\detect\train_high_Res\weights\best.pt"
    model = YOLO(model_dir, task="detect")
    img_dir = "../custom_dataset/test/full\\"
    for img in os.listdir(dir+img_dir):
        if img.endswith(".jpg") or img.endswith(".png"):
            path = dir+img_dir + img

            results = model.predict(path, save=False, conf=0.5)

            for result in results:
                i = 0
                image = Image.open(path)
                cords = torch.round(result.boxes.xyxy).to(torch.int)
                for x in cords:
                    i += 1
                    box = image.crop(x.tolist())
                    # print(box.size)
                    if box.size[0] >= 65 and box.size[1] >= 65:  # may change based on the kind of data and resolution (further testing)
                        if not box.size[0]*2.5 < box.size[1] and not box.size[1]*2.5 < box.size[0]:  # prevents extremely wide but very short or extremely long but very narrow images to appearing
                            box.save("test_result\\"+img[:]+"__"+str(i)+".jpg", verbose=0)

        else:
            print("Wrong format")


def detect_with_image(img):
    dir = os.getcwd()
    model_dir = dir + r"\runs\detect\train_high_Res\weights\best.pt"
    model = YOLO(model_dir, task="detect")
    results = model.predict(img, save=False, conf=0.5)
    images = []
    for result in results:
        cords = torch.round(result.boxes.xyxy).to(torch.int)
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            if x2-x1 >= 65 and y2-y1 >= 65:
                if (x2-x1) * 2.5 > y2-y1 and (y2-y1) * 2.5 > x2-x1:  # prevents extremely wide but very short or extremely long but very narrow images to appearing
                    cropped_object = img.crop((x1, y1, x2, y2))
                    print("x1="+str(x1)+" x2="+str(x2)+" y1="+str(y1)+" y2="+str(y2))
                    images.append(cropped_object)

        # for x in cords:
        #     box = img.crop(x.tolist())
        #     if box.size[0] >= 65 and box.size[1] >= 65:  # may change based on the kind of data and resolution (further testing)
        #         if (not box.size[0] * 2.5 < box.size[1]
        #                 and not box.size[1] * 2.5 < box.size[0]):  # prevents extremely wide but very short or extremely long but very narrow images to appearing
        #             print(img)
        #             images.append(img)

    return images
