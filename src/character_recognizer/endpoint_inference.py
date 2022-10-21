"""Script to send randomly selected MNIST test images in batches of 10 to the
inference endpoint and get the predictions.
"""

import os
from pathlib import Path
import random

import requests

INFERENCE_URL = "http://localhost:8080/predictions/mnist"
TEST_IMAGES_DIR = Path(
    "/Users/sanjeev/Career/MLinProduction/my_projects/handwritten_text_recognizer_EN/dataset/MNIST/sample_images"
)
NB_IMAGES = 50

targets = []  # the true labels
predictions = []  # predicted labels
sample_images = os.listdir(TEST_IMAGES_DIR)
random.shuffle(sample_images)  # in-place shuffle
for image in sample_images[:NB_IMAGES]:
    with open(TEST_IMAGES_DIR / image, "rb") as f:
        response = requests.post(INFERENCE_URL, data=f)
    predictions.append(response.text)
    targets.append(image[-5])

print("Predicted  Actual")
for p, t in zip(predictions, targets):
    print(f"    {p}        {t}")
