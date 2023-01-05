###############################################################################
# Makefile for running Docker container
# with pyenv, pdm, PyData Stack, JupyterLab + more
# See documentation in original Dockerfile for more information.
#
# Maintainer: Goopy Flux <goopy.flux@gmail.com>
###############################################################################

# Note: Update the image tag if the Dockerfile changes
# Local Image
image_name = puppydog
image_tag = latest
local_image = ${image_name}:${image_tag}

# Remote Repository on Docker Hub
docker_hub_repo = goopyflux/puppydog
remote_image = ${image_name}:${image_tag}

# #############
# make commands
# #############

# Host volume to mount
host_volume ?= ${PWD}

# Name for the Docker container
container_name = written_text

# Note: delete the --rm option, if you wish to persist the container upon exit.
# Ex. may be to call `docker commit` to save the container as a new image.
## Run the JupyterLab Docker container. Use host_volume to specify local folder.
## (Ex. make docker-run host_volume=/home/user/work)
docker-run:
	docker run -it --init -p 8888:8888 -v "${host_volume}:/root/work" --name ${container_name} ${local_image}

## Start the previously stopped container
docker-start:
	docker container start ${container_name}

## Connect to the running instance of the Docker container from the command line
docker-exec:
	docker exec -it ${container_name} /bin/bash

## Push the latest commits to remote GitHub repo (assumed to be setup).
git-push:
	git push -u origin main

serve_container = tserve
## Serve the model using TorchServe Docker Container
serve:
	docker run -it --name $(serve_container) -p 8080:8080 -p 8081:8081 -p 8082:8082 -p 7070:7070 -p 7071:7071 -v ${PWD}/artifacts:/home/model-server/model-store -v ${PWD}/src:/home/model-server/src -v ${PWD}/torchserve:/home/model-server/torchserve -v ${PWD}/logs:/home/model-server/logs pytorch/torchserve

## Start a previously stopped tserve container
serve-start:
	docker container start ${serve_container}

## Access the running instance of the TorchServe Image
serve-exec:
	docker exec -it ${serve_container} /bin/bash

model_name = mnist
model_version = 1.0
## Create model archive file (do this only after accessing the Torchserve container)
mar:
	pdm run torch-model-archiver --model-name ${model_name} --version ${model_version} --model-file src/character_recognizer/mnist.py --serialized-file artifacts/mnist_cnn.pt --export-path artifacts --handler torchserve/mnist_handler.py

test_folder = tests
## Run tests
pytest:
	pdm run pytest ${test_folder}

py_dirs = src scripts tests web_app torchserve

## Automatic code formatting with Black
black:
	pdm run black ${py_dirs}

## Check code style with Flake8
flake:
	pdm run flake8 ${py_dirs}

## Format and Style code in one-step
lint: black flake

tserve_url = http://127.0.0.1
models_port = 8081
model_url = artifacts/mnist.mar
num_workers = 2
## Register model with a running instance of Torchserve
register-model:
	curl -X POST "${tserve_url}:${models_port}/models?initial_workers=${num_workers}&synchronous=false&url=${model_url}"

## Build HTML docs using Sphinx
html:
	pdm run sphinx-build -b html . _build

venv:
	python -m venv venv

SHELL := /bin/bash
pip:
	source venv/bin/activate && \
	python -m pip install --upgrade pip setuptools wheel && \
	python -m pip install -e . && \
	pre-commit install && \
	pre-commit autoupdate && \
	pre-commit run --all-files

## Create a virtual environment and install everything needed to run locally
venv_pip: venv pip

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')

