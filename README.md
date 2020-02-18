# CPS-IoT Week Competition
Welcome to AiFi's CPS-IoT Autocheckout Competition. This document details the competition and will help you get started.

## Overview
This repository will help you get started with examples on how to use the Public Datasets available at http://aifi.io/research under Sample Data.

To start please download the data labelled as: "Simple Example" without depth (For your first example).

During the competition you will need a competitor token that will distinguish your submission from all other competitors. However you dos
o not need this token for your local testing environment.

## Sample Data

In order for the example to work properly download the data into `data/donwloads`.

### Simple Example
Download Videos [Here](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-01/cps-test-videos.gz) (17.1MB)

Download Data without Depth Images [Here](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-01/cps-test-01-nodepth.archive) (239MB)

Download Data with Depth Images [Here](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-01/cps-test-01-all.archive) (2.0GB)

### Multiple People Dataset

| Left-aligned | Center-aligned | Right-aligned |
| :---         |     :---:      |          ---: |
| git status   | git status     | git status    |
| git diff     | git diff       | git diff      |




| Test Case | Video | Data w/ Depth | Data w/o Depth |
| :---: | :---: | :---: | :---: | :---: |
| Simple Case | [Donwload](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-01/cps-test-videos.gz?authuser=1) |  [Download](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-01/cps-test-01-all.archive?authuser=1) | [Download](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-01/cps-test-01-nodepth.archive?authuser=1) |


## Getting Started

### Obtain a competitor token
After submitting your abstract describing your approach You will receive a competitor token.
Do not share your token with anyone outside your team. It will be used to uniquely identify you, access test cases, and to submit your results.
Set it to an env variable for later use.
```
export AIFI_CPSWEEK_COMP__TOKEN=<your-token>
```

### Dependencies
Before you begin, you will need to setup a few dependencies:
- *`docker`*: [Install Docker](https://docs.docker.com/install/)
- *`docker-compose`*: [Install `docker-compose`](https://docs.docker.com/compose/install/)

### Clone
This repo provides everything you need to get started. Begin by cloning this repo.
```
# Clone the repo
git clone git@gitlab.com:aifi-ml/aifi-public/cpsweek.git
cd cpsweek/
```

### Test
After you have cloned the repo, you can execute the solution against an example and print the results with the following command.
```
AIFI_CPSWEEK_COMP__COMMAND=cps-test-01 docker-compose up --build
```

### Submit
You will be able to submit your solution after you have submitted your abstract and received a competitor token.

## FAQ
Before contacting AiFi, check the frequently asked questions below.

### I saw this error:
- `PermissionError: [Errno 13] Permission denied:`
  - The files backing the mongodb are owned by a user you do not have permissions to access. Run the `docker-compose` with `sudo`

### Can I add my own dependencies?
Yes. Just add them to `requirements.txt`.

### Can I use a GPU acceleration?
Yes. See Docker's guide on leveraging GPU in docker containers.

### The docker compose never returns!
You can send a SIGTERM to the program while it's in the foreground with ctrl-C or you can run the `docker-compose` command with the option `--abort-on-container-exit`
