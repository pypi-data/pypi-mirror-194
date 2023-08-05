# Python project boiler plate

This project aims to make the building, and deployment of python packages and docker containers using OneDev as simple as possible.

## Features

- publish to docker hub
- publish to pypi
- sync with github

## How to Setup

- Make a copy/fork of this repository
- Update the following values in setup.py:
    - name
    - version
    - description
    - author
    - license
    - classifiers
    - install requires
    - extras_require
- Update the docker file:
    - add your contact info to the `MAINTAINER` line
    - `CMD` to whatever command starts your app
- In OneDev:
    - Edit step templates in the `.onedev-buildspec.yaml` file::
        - Execute tests:Run Pytest:
            - add command to run test suite(s) if not pytest
        - Publish Docker Container to Dockerhub: publish to dockerhub:
            - update username to your dockerhub username
    - Under `Settings > Build > Job Secrets` add
      - your docker hub password as `docker_hub_password`
      - your docker hub password as `docker_hub_user`
      - your pypi password as `pypi_password`
      - your pypi user as `pypi_user`
    - If there isn't already, make a 'Server Docker Executor' called `docker-executor` under `Administration > Job Executors`
- fill in your `README.md` and remove this section

----

# My Project

Describe what your package is about

## Package Distribution

### Installation

`pip install my-project`

### Use

`python ./src/main.py`

## Docker Distibution

### Installation

`docker pull docker_user/project_name:latest`

### Use

`docker run -p 5000:5000 project_name`

or for detached mode:

`docker run -d -p 5000:5000 project_name`

