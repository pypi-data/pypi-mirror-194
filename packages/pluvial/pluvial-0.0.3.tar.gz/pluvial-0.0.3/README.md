# pluvial

Pluvial is a Python package for generating static websites from markdown files, born out of a rainy day project. The name "pluvial" was chosen as a nod to the day the project was started, which happened to be a particularly rainy day.

## Local Setup

### Install Miniconda

For installers for operating systems other than linux see https://docs.conda.io/en/latest/miniconda.html

    curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -s --output miniconda.sh
    chmod +x miniconda.sh
    ./miniconda.sh -u
    rm miniconda.sh

### Create conda enviroment

You may need to reopen your shell after installing miniconda

    conda create -n pluvial python=3.10
    conda activate pluvial
    conda install --file requirements.txt

### Run the project

The default port is 5000

    python ./app/main.py

## Docker

### Building the Docker container

With your working directory in the root of the repository

    docker build --tag pluvial .

### Running the Docker container

    docker run -p 5000:5000 pluvial

or for detached mode

    docker run -d -p 5000:5000 pluvial    


### Publishing to docker

    docker login
    docker build --tag mullinmax/pluvial:latest .
    docker push mullinmax/pluvial:latest
