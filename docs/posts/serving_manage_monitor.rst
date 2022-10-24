###############################################
Serve, Manage and Monitor Model with TorchServe
###############################################

Usage
=====

Steps for creating the model archive locally
--------------------------------------------

.. note::

   Make sure to `pip install torch-model-archiver` before proceeding.

- Start the local development Docker container with all necessary dependencies installed by running `make docker-run`. If Docker complains that there is already an instance of the same name then run either 1. `make docker-start` or 2. `make docker-run container_name=another_dev_container` or 3. skip this step all together if the container is already running (`docker ps` to double check).
- Connect to the terminal on the remote container by running `make docker-exec` or `make docker-exec container_name=what_was_used_above`
- Create a Torchserve model archive file by running `make mar` (options here include `model_name` and `model_version`). Find the compiled `mar` file in the `artifacts` folder.


Steps for running inference locally
-----------------------------------

- Start the Torchserve Docker container by running `make serve-run` or `make serve-start`, if the container was previously run.
- Register the model by running `make register-model`. Options here include `tserve_url`, `models_port`, `num_workers` and `model_url`.


A Short Introduction to Torchserve
==================================

Torchserve has Java dependencies, amongst others. To get up and running I will use the official Docker image to run TorchServe as a Docker container that can be accessed via the REST API.

IMO, this is also a point to draw a line between DevOps/MLOps responsibilities vs. Data Science/ML Engineer responsibilities.

**Prerequisites**: `Docker <https://www.docker.com/>`_

Get the official TorchServe Docker image
----------------------------------------

Pull the latest TorchServe image from Docker Hub. By default, the latest tag is the same as latest-cpu.::

   docker pull pytorch/torchserve

Start a Docker container using the image
----------------------------------------

A note on Docker containers and storage - It's generally a good idea to think about storage, since Docker containers are ephemeral(??) and cannot be accessed once the container is destroyed. Be sure the mount the relevant local folder to access to data even after the container is not available.

.. code:: bash

   # Mount folders containing model-store, model-file, model-state-dict and logs
   # Expose ports 8080-8082 and 7070-7071 for access to various REST APIs
   docker run -it --rm -p 8080:8080 \
           -p 8081:8081 \
           -p 8082:8082 \
           -p 7070:7070
           -p 7071:7071
           --name torchserve \
           -v artifacts:/home/model-server/model-store \
           -v src:/home/model-server/src \
           -v torchserve:/home/model-server/torchserve \
           -v logs:/home/modelserver/logs \
           pytorch/torchserv-latest

This will start the Docker image. Assuming the image started without any issues, the server can be tested with::

        curl http://localhost:8080/ping

which should respond with::

        {
          "status": "Healthy"
        }

Now we are good to go!

Generate a model archive (.mar) file
------------------------------------

<Add blurb about mar files here.>

TorchServe comes with tools to help package the model artifacts into a single model archive file (`*.mar`). Since this will run on the TorchServe container, we will first access the Docker image via CLI.::

        docker exec -it torchserve /bin/bash

This assumes that the Docker image was started with `--name torchserve` argument.

Create the `mar` file using::

        torch-model-archiver --model-name mnist \
                --version 1.0 \
                --model-file src/character_recognizer/mnist.py
                --serialized-file artifacts/mnist_cnn.pt \
                --export-path /home/model-server/model-store \
                --handler torchserve/mnist_handler.py

Register the model archive
--------------------------

Torchserve needs to know about the models and provides a `model API <https://pytorch.org/serve/management_api.html>`_ to manage models (and much more!).

Register the model by::

        curl -X POST "http://localhost:8081/models?url=artifacts/mnist.mar"

The response looks like this.::

        {
          "status": "Model \"mnist\" Version: 1.0 registered with 0 initial workers. Use scale workers API to add workers for the model."
        }

Note that this will only register but not start any workers, i.e., no inference point yet (as indicated in the response message above).

There are two options here -

1. Register the model (as above) and subsequently make a separate API call to scale worker(s) as::

        curl -X PUT "http://localhost:8081/models/mnist?min_workers=1"

2. Combine the two into a single call at registration as::

        curl -X POST "http://localhost:8081/models?initial_workers=1&synchronous=false&url=artifacts/mnist.mar"

Check the model by accessing the models API.::

        curl http://localhost:8081/models

The response should look like::

        {
          "models": [
            {
              "modelName": "mnist",
              "modelUrl": "artifacts/mnist.mar"
            }
          ]
        }

Attempting to re-register an existing model can result in a `ConflictStatusException` as shown in the response below.::

        {
          "code": 409,
          "type": "ConflictStatusException",
          "message": "Model version 1.0 is already registered for model mnist"
        }

To deregister a model, use::

        curl -X DELETE "http://localhost:8081/models/mnist/1.0"

The response should look like.::

        {
          "status": "Model \"mnist\" unregistered"
        }

Querying the Inference Endpoint
-------------------------------

The inference endpoint is available at `http://localhost:8080/predictions/mnist` and it accepts an image file, which can be `curl`ed with the `-T` option as below.::

        curl "http://localhost:8080/predictions/mnist" -T datasets/MNIST/sample_images.0.png

The response should be the predicted class (as a string), which in this instance will be `0`.

Let us run inference on a random sampling of images using a simple Python script.

.. code:: python

   import os
   from pathlib import Path
   import random
   import requests

   INFERENCE_URL = "http://localhost:8080/predictions/mnist"
   TEST_IMAGES_DIR = "dataset/MNIST/sample_images"
   NB_IMAGES = 10

   targets = []  # the true labels
   predictions = []  # predicted labels
   sample_images = os.listdir(TEST_IMAGES_DIR)
   random.shuffle(sample_images)  # in-place shuffle
   for image in sample_images[:NB_IMAGES]:
       with open(image, "rb") as f:
           response = requests.post(INFERENCE_URL, data=f)
       predictions.append(response.text)
       targets.append(image[-5])  # get output label from the name

   print("Predicted  Actual")
   for p, t in zip(predictions, targets):
       print(f"{p}        {t}")

It prints out::

        Predicted  Actual
            9        9
            7        7
            7        7
            3        3
            8        8
            7        7
            0        0
            5        5
            7        7
            5        5

After running this script a few times, we can go over to the metrics API to get some stats on how the endpoint is performing.

Metrics
-------

The metrics API is available at port `8082` and can accessed by the URL `http://localhost:8082/metrics`

The default metrics available are::

        # HELP ts_inference_requests_total Total number of inference requests.
        # TYPE ts_inference_requests_total counter
        ts_inference_requests_total{uuid="7f843173-4784-4bde-a04e-524c37f4f918",model_name="mnist",model_version="default",} 24.0
        # HELP ts_queue_latency_microseconds Cumulative queue duration in microseconds
        # TYPE ts_queue_latency_microseconds counter
        ts_queue_latency_microseconds{uuid="7f843173-4784-4bde-a04e-524c37f4f918",model_name="mnist",model_version="default",} 10568.457999999999
        # HELP ts_inference_latency_microseconds Cumulative inference duration in microseconds
        # TYPE ts_inference_latency_microseconds counter
        ts_inference_latency_microseconds{uuid="7f843173-4784-4bde-a04e-524c37f4f918",model_name="mnist",model_version="default",} 591362.951

Next steps - setup `Prometheus <https://prometheus.io/docs/prometheus/latest/getting_started/>`_ for storing time-series logs of the metrics and possibly use `Grafana <https://prometheus.io/docs/visualization/grafana/>`_ to setup dashboards and visualize graphs.

Below are the metrics with a single worker on a Docker container after images in batches of 10, 10, 10, 50.

        # HELP ts_inference_latency_microseconds Cumulative inference duration in microseconds
        # TYPE ts_inference_latency_microseconds counter
        ts_inference_latency_microseconds{uuid="9ed569e2-3b0a-4435-b63e-cfd5e57449f5",model_name="mnist",model_version="default",} 7485497.346000001
        # HELP ts_inference_requests_total Total number of inference requests.
        # TYPE ts_inference_requests_total counter
        ts_inference_requests_total{uuid="9ed569e2-3b0a-4435-b63e-cfd5e57449f5",model_name="mnist",model_version="default",} 80.0
        # HELP ts_queue_latency_microseconds Cumulative queue duration in microseconds
        # TYPE ts_queue_latency_microseconds counter
        ts_queue_latency_microseconds{uuid="9ed569e2-3b0a-4435-b63e-cfd5e57449f5",model_name="mnist",model_version="default",} 775792.99

Below are the metrics with a four worker on a Docker container after images in batches of 10, 10, 10, 50.

        # HELP ts_inference_latency_microseconds Cumulative inference duration in microseconds
        # TYPE ts_inference_latency_microseconds counter
        ts_inference_latency_microseconds{uuid="b7a0cfbf-eaf7-4615-b3af-6f0178fcdaf0",model_name="mnist",model_version="default",} 7065172.445999999
        # HELP ts_inference_requests_total Total number of inference requests.
        # TYPE ts_inference_requests_total counter
        ts_inference_requests_total{uuid="b7a0cfbf-eaf7-4615-b3af-6f0178fcdaf0",model_name="mnist",model_version="default",} 80.0
        # HELP ts_queue_latency_microseconds Cumulative queue duration in microseconds
        # TYPE ts_queue_latency_microseconds counter
        ts_queue_latency_microseconds{uuid="b7a0cfbf-eaf7-4615-b3af-6f0178fcdaf0",model_name="mnist",model_version="default",} 69264.58100000002

References:
===========

- `TorchServe Docker docs <https://github.com/pytorch/serve/blob/master/docker/README.md>`_
- `Example MNIST inference <https://github.com/pytorch/serve/tree/master/examples/image_classifier/mnist>`_
- `Management API docs <https://pytorch.org/serve/management_api.html>`_
- `Metrics API docs <https://pytorch.org/serve/metrics_api.html>`_
- `Pillow documentation <https://pillow.readthedocs.io/en/stable/handbook/tutorial.html>`_

