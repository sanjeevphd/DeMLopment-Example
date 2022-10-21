import csv
from datetime import datetime
import io
import os
from pathlib import Path
from time import time
import uuid

from PIL import Image
from torch.profiler import ProfilerActivity
from torchvision import transforms
from ts.torch_handler.image_classifier import ImageClassifier


class MNISTDigitClassifier(ImageClassifier):
    """
    MNISTDigitClassifier handler class. This handler extends class ImageClassifier from image_classifier.py, a
    default handler. This handler takes an image and returns the number in that image.

    Here method postprocess() has been overridden while others are reused from parent class.
    """

    image_processing = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])

    class MNISTLogger:
        """Custom logger class for MNIST inference.

        Saves a CSV log with each row corresponding to an inference request and
        the corresponding prediction.
        Saves the raw input image data to a folder using UUID for file name.
        """

        LOGGING_DIR = Path("/home/model-server/logs")
        DEFAULT_HEADER = "Time,Image,Prediction,Latency".split(",")

        def __init__(self, header=None, logging_dir=None):
            if logging_dir is None:
                logging_dir = self.LOGGING_DIR

            if header is None:
                header = self.DEFAULT_HEADER

            self.image_dir = logging_dir / "input_images"
            self.log_filepath = logging_dir / "inference_io.csv"

            if not os.path.exists(self.image_dir):
                os.mkdir(self.image_dir)

            with open(self.log_filepath, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(header)

        def log(self, data, parameters):
            # Convert raw data (list) to PIL.Image
            img = Image.open(io.BytesIO(data[0].get("body")))

            # Generate a random UUID for the image file name
            img_path = self.image_dir / f"{uuid.uuid4()}.png"
            img.save(img_path)

            # Format row
            # Get time
            time_str = datetime.now().__str__()
            csv_row = [time_str, img_path] + parameters

            # Append row to CSV log file
            with open(self.log_filepath, "a", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(csv_row)

    def __init__(self):
        super(MNISTDigitClassifier, self).__init__()
        self.profiler_args = {
            "activities": [ProfilerActivity.CPU],
            "record_shapes": True,
        }
        self.mnist_logger = self.MNISTLogger()

    def handle(self, data, context):
        """Entry point for default handler. It takes the data from the input
        request and returns the predicted outcome for the input.

        Parameters
        ----------
        data: list
              The input data that needs to be made a prediction request on.

        context: Context
                 It is a JSON Object containing information pertaining to
                 the model artifacts parameters.

        Returns
        -------
            pred_out: list
                      list of dictionary with the predicted response.

        """
        start = time()
        preprocess_data = self.preprocess(data)
        pred_out = self.model.forward(preprocess_data)
        latency_time = time() - start
        pred_label = self.postprocess(pred_out)
        self.mnist_logger.log(data, pred_label + [latency_time])
        return pred_label

    def postprocess(self, data):
        """The post process of MNIST converts the predicted output response to a label.

        Parameters
        ----------
        data : list
               The predicted output from the Inference with probabilities is passed to the post-process function

        Returns
        -------
        labels : list
               A list of dictionaries with predictions and explanations is returned
        """
        labels = data.argmax(1).tolist()

        return labels
