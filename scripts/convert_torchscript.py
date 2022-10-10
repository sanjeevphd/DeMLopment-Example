from pathlib import Path

from character_recognizer.mnist import SimpleCNN
import torch

ARTIFACT_PATH = Path("../artifacts")


def save_model_artifact(model, artifact_path):
    # Convert model to a torchscript ScriptModule
    model_script_module = torch.jit.script(model)

    # Save to file
    torch.jit.save(model_script_module, artifact_path)
    print(f"Model: {model}")
    print(f"Saved to: {artifact_path}")


artifact_path = ARTIFACT_PATH / "SimpleCNN_mnist_jit.pt"
simple_cnn = SimpleCNN()
save_model_artifact(simple_cnn, artifact_path)
