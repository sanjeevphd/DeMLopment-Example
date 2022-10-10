# Utility functions

from PIL import Image
from torchvision import transforms


def read_image(image_path):
    img = Image.open(image_path)
    return img


def transform_raw_image(image_data):
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])

    return transform(image_data)
