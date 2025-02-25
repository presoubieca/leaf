import model
import tensorflow as tf
import os
import numpy as np

def classify_web(img):
    imgs = model.detect_with_image(img)
    if imgs is not None:
        di = os.getcwd()
        print(print(tf.__version__))
        loaded_model = tf.keras.models.load_model(r'models\Sick_or_Not_1.11.keras')
        # trues = 311
        # falses = 124
        # trues = 7228
        # falses = 3672
        # using 1.2
        ls = []
        images = []
        # TEST
        for img in imgs:
            #img = tf.keras.preprocessing.image.load_img(img, target_size=(256, 256))
            img_array = tf.keras.preprocessing.image.img_to_array(img)

            img_array = np.expand_dims(img_array, axis=0)
            img_tensor = tf.convert_to_tensor(img_array)

            res = loaded_model.predict(img_tensor)

            if res[0][0] > 0.5:
                ls.append("Sick")
            else:

                ls.append("Healthy")

            images.append(img)

        return ls, images
        # print("------------------- -----------")


def classify_desktop(img):
    img = model.detect_with_image(img)
    if img is not None:
        class_name = ["Healthy", "Sick"]
        dire = os.getcwd()
        loaded_model = tf.keras.models.load_model(r'Sick_or_Not_models/Sick_or_Not_1.11.keras')
        # trues = 311
        # falses = 124
        # trues = 7228
        # falses = 3672
        # using 1.2

        # TEST
        trues = 0
        falses = 0
        for name in class_name:
            test_dir_name = "Healthy\\" + name

            for filename in os.listdir(test_dir_name):

                img_path = dire + "\\" + test_dir_name + "\\" + filename

                img = tf.keras.preprocessing.image.load_img(img_path, target_size=(256, 256))
                img_array = tf.keras.preprocessing.image.img_to_array(img)

                img_array = np.expand_dims(img_array, axis=0)
                img_tensor = tf.convert_to_tensor(img_array)

                res = loaded_model.predict(img_tensor)
                print(res)

                if res[0][0] < 0.5:
                    ls = "Sick"
                else:
                    ls = "Healthy"

                if ls == name:
                    trues += 1
                else:
                    falses += 1
                # print("------------------- -----------")

        print("trues = "+str(trues))
        print("falses = "+str(falses))



def iterate_over_images(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff")):
                classify_desktop(file)

if __name__ == "__main__":
    root_directory = "images_512/test"  # Change this to your target directory
    iterate_over_images(root_directory)
