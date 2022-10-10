# Image Transform class to transform raw image to tensors for inference
import character_recognizer.utils as utils


class TransformCharacterImage:
    """A class for handling image transforms."""

    def __init__(self):
        self.transforms = utils.transform_raw_image  # transforms.Compose([])

    def __call__(self, image):
        timg = self.transforms(image)

        return timg
