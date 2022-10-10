"""Script for testing inference."""

import os
from pathlib import Path
import random

from character_recognizer.inference import WrittenCharacterRecognizer
from character_recognizer.transform import TransformCharacterImage

# Configuration
IMAGE_PATH = Path("./dataset/MNIST/sample_images")
sample_images = os.listdir(IMAGE_PATH)

NB_CLASSES = 10
output_labels = list("0123456789")


class TestWrittenCharacterRecognizer:
    """Main class for testing."""

    def testInstance(self):
        character_recognizer = WrittenCharacterRecognizer(transforms=TransformCharacterImage())
        assert character_recognizer.model.__str__().startswith("RecursiveScriptModule")
        pred = character_recognizer.predict(IMAGE_PATH / random.choice(sample_images))
        assert pred in output_labels
