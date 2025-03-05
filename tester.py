import model
import tensorflow as tf
import os
import numpy as np

def classify_web(img):
    imgs = model.detect_with_image(img)
    if imgs is not None:
        di = os.getcwd()
        loaded_model = tf.keras.models.load_model(r'models\Sick_or_Not_1.11.keras') # loading model

        ls = []
        images = []
        # TEST
        for img in imgs:

            # Preparing images for classification
            img_array = tf.keras.preprocessing.image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_tensor = tf.convert_to_tensor(img_array)

            # Classifying images
            res = loaded_model.predict(img_tensor)

            if res[0][1] <= 0.87:
                print(str(res[0][0])+"sick")
                print(str(res[0][1])+"sick")

                ls.append("Sick")
            else:
                print(str(res[0][0])+"healthy")
                print(str(res[0][1])+"healthy")

                ls.append("Healthy")

            images.append(img)

        return ls, images

def iterate_over_images(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff")):
                classify_desktop(file)

if __name__ == "__main__":
    root_directory = "images_512/test"
    iterate_over_images(root_directory)
