##############################
Machine Learning in Production
##############################

An example of a full stack, production grade, machine learning engineering.

Overview
========

Let me break down the one-liner above.

- full stack - all the way from problem understanding, data mgmt., model development, to deployment, monitoring and retraining
- production grade - it has to add value, in a business sense and can grow and scale with the business
- machine learning engineering - employ best practices rooted in software engineering principles
- example - demonstrate with a concrete use case, which might be trivial but captures the essence of process

Approach/Methodology
====================

- start at the end
- test-driven development
- agile mindset - small changes, rapid iterations, steady progress
- cloud-ready local development
- automate the automatable

Usage
=====

There are several offerings here.

The Docker Way
--------------

This is the *no hassle* offering. The only requirement is `Docker <http://www.docker.com>`_.

        `docker run -it demlopment:latest`

.. note::

   Update to the Docker command

The Docker Dashboard should reveal the container orchestration behind the scene that reflects the three major domains that come together to make the magic happen.

#. An inference endpoint that uses Torchserve for model managment, metrics, deployment, A/B testing, etc.
#. A development environment for model development. Everything from data loading, splitting, training, validation, hyperparameter tuning, experiment tracking to testing and model selection
#. A data management environment for ingesting, storing and transforming data

Any or all of the three domains can be cloud-native or local/on-premisis depending on the use case. At *reasonable scales*, it is "reasonable" to assume that all domains are cloud native. My view is that as a data scientist, ML engineer, DL scientist, most time is spent in the model domain and a local development makes perfect sense, while *outsourcing* the data management and model deployment to the cloud. This allows for faster iterations and even potentially avoids some yak shaving.

Local Installation
------------------

- Clone the GitHub repo.

        `git clone <repo_url>`

- Install the dependencies and the package in a local virtual environment.

        `make venv_pip`

  .. note::
     Update requirements to include `pytest`.

- Run tests

        `python -m pytest tests`

Documentation
=============

- `Motivation and Introduction <docs/posts/deMLopment.rst>`_
- `Begin with the end in mind - Create an endpoint <docs/posts/endpoint.rst>`_
- `Serve and run inference using Torchserve in a Docker container <docs/posts/serving_manage_monitor.rst>`_
