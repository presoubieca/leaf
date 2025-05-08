import model as md
import os
import numpy as np
import torch
from torchvision.models import resnet18
from torchvision import transforms
from PIL import Image

def classify_web(img):
    imgs = md.detect_with_image(img)
    model = resnet18()
    model.fc = torch.nn.Linear(model.fc.in_features, 2)  # Match number of output classes
    model.load_state_dict(torch.load('models/torchV1.2.pth', map_location='cpu'))
    model.eval()

    # Define preprocessing (resize to 256x256)
    preprocess = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])
    if imgs is None:
        return [], []

    ls = []
    images = []

    for img in imgs:

        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Preprocess image
        input_tensor = preprocess(img).unsqueeze(0)  # Shape: [1, 3, 256, 256]

        # Inference
        with torch.no_grad():
            output = model(input_tensor)
            probs = torch.nn.functional.softmax(output, dim=1)
            prob_healthy = probs[0][0].item() # probs[0][0] = how healthy probs probs[0][1] = how sick

        # Classify based on threshold

        if prob_healthy <= 0.99:
            print(f"{probs[0][0].item():.4f} sick")
            print(f"{probs[0][1].item():.4f} sick")

            ls.append("Sick")
        else:
            print(f"{probs[0][0].item():.4f} healthy")
            print(f"{probs[0][1].item():.4f} healthy")

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
