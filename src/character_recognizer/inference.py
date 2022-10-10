# Image recognition class to carry out inference

from pathlib import Path

from character_recognizer.transform import TransformCharacterImage
import character_recognizer.utils as utils
import torch
import typer

MODEL_PATH = Path(__file__).resolve().parents[2] / "artifacts" / "SimpleCNN_mnist_jit.pt"


def load_model(jit_model_path):
    model = None
    try:
        model = torch.jit.load(jit_model_path)
    except RuntimeError:
        print(f"Unrecognized model format. Expecting model in TorchScript format." f"{jit_model_path}")

    return model


PREDICTION_STRING = "Prediction"


def convert_pred_to_string(pred):
    if pred is not None:
        return str(pred.item())
    return PREDICTION_STRING


class WrittenCharacterRecognizer:
    """Class for written character recognition inference."""

    def __init__(self, transforms=None):
        self.model = load_model(MODEL_PATH)
        self.transforms = transforms

    def predict(self, image):
        if self.model is None:
            print("No model found.")
            return None

        image_data = utils.read_image(image)
        pred = None
        if self.transforms is not None:
            image_tensor = self.transforms(image_data).unsqueeze(axis=0)
            if isinstance(image_tensor, torch.Tensor):
                output = self.model(image_tensor)
                pred = output.argmax(dim=1, keepdim=True)
            else:
                pred = None
        pred_str = convert_pred_to_string(pred)

        return pred_str


def main(image_path):
    character_recognizer = WrittenCharacterRecognizer(transforms=TransformCharacterImage())
    pred = character_recognizer.predict(image_path)
    print(f"{pred}")


if __name__ == "__main__":
    typer.run(main)
