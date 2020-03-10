# CPS-IoT Week Competition
Welcome to AiFi's CPS-IoT Autocheckout Competition. This document details the competition and will help you get started.

## Overview
This repository will help you get started with examples on how to use the Public Datasets available at http://aifi.io/research under Sample Data.

To start please download the data labelled as: "Simple Example" without depth (For your first example).

During the competition you will need a competitor token that will distinguish your submission from all other competitors. However you do
not need this token for your local testing environment.

## Sample Data

In order for the example to work properly download the data into `data/downloads`.

### Simple Example
Download Videos [Here](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-01/cps-test-videos.gz) (17.1MB)

Download Data without Depth Images [Here](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-01/cps-test-01-nodepth.archive) (239MB)

Download Data with Depth Images [Here](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-01/cps-test-01-all.archive) (2.0GB)

### Multiple People Dataset

Test Case | Video | Data w/ Depth| Data w/o Depth | Camera Calibration
---|---|---|---|---
Simple Case | [Donwload](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-01/cps-test-videos.gz?authuser=1) |  [Download](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-01/cps-test-01-all.archive?authuser=1) | [Download](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-01/cps-test-01-nodepth.archive?authuser=1) | [Download](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/calibration/cps_week_test_cases_1-1_camera_calibration.json)
| Test 2 | Coming Soon |  [Download](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-02/cps-test-02-all.archive?authuser=1) | Coming Soon | [Download](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/calibration/cps_week_test_cases_2-24_camera_calibration.json)
| Test 3 | Coming Soon |  [Download](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-03/cps-test-03-all.archive?authuser=1) | Coming Soon | [Download](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/calibration/cps_week_test_cases_2-24_camera_calibration.json)
| Test 4 | Coming Soon |  [Download](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-04/cps-test-04-all.archive?authuser=1) | Coming Soon | [Download](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/calibration/cps_week_test_cases_2-24_camera_calibration.json)
| Test 5 | Coming Soon |  [Download](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-05/cps-test-05-all.archive?authuser=1) | Coming Soon | [Download](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/calibration/cps_week_test_cases_2-24_camera_calibration.json)
| Test 6 | Coming Soon |  [Download](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-06/cps-test-06-all.archive?authuser=1) | Coming Soon | [Download](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/calibration/cps_week_test_cases_2-24_camera_calibration.json)
| Test 7 | Coming Soon |  [Download](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-07/cps-test-07-all.archive?authuser=1) | Coming Soon | [Download](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/calibration/cps_week_test_cases_2-24_camera_calibration.json)
| Test 8 | Coming Soon |  [Download](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-08/cps-test-08-all.archive?authuser=1) | Coming Soon | [Download](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/calibration/cps_week_test_cases_2-24_camera_calibration.json)
| Test 9 | Coming Soon |  [Download](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-09/cps-test-09-all.archive?authuser=1) | Coming Soon | [Download](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/calibration/cps_week_test_cases_2-24_camera_calibration.json)
| Test 10 | Coming Soon |  [Download](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-10/cps-test-10-all.archive?authuser=1) | Coming Soon | [Download](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/calibration/cps_week_test_cases_2-24_camera_calibration.json)
| Test 11 | Coming Soon |  [Download](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-11/cps-test-11-all.archive?authuser=1) | Coming Soon | [Download](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/calibration/cps_week_test_cases_2-24_camera_calibration.json)
| Test 12 | Coming Soon |  [Download](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-12/cps-test-12-all.archive?authuser=1) | Coming Soon | [Download](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/calibration/cps_week_test_cases_2-24_camera_calibration.json)
| Test 13 | Coming Soon |  [Download](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-13/cps-test-13-all.archive?authuser=1) | Coming Soon | [Download](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/calibration/cps_week_test_cases_2-24_camera_calibration.json)
| Test 14 | Coming Soon |  [Download](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-14/cps-test-14-all.archive?authuser=1) | Coming Soon | [Download](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/calibration/cps_week_test_cases_2-24_camera_calibration.json)
| Test 15 | Coming Soon |  [Download](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-15/cps-test-15-all.archive?authuser=1) | Coming Soon | [Download](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/calibration/cps_week_test_cases_2-24_camera_calibration.json)
| Test 16 | Coming Soon |  [Download](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-16/cps-test-16-all.archive?authuser=1) | Coming Soon | [Download](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/calibration/cps_week_test_cases_2-24_camera_calibration.json)
| Test 17 | Coming Soon |  [Download](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-17/cps-test-17-all.archive?authuser=1) | Coming Soon | [Download](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/calibration/cps_week_test_cases_2-24_camera_calibration.json)
| Test 18 | Coming Soon |  [Download](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-18/cps-test-18-all.archive?authuser=1) | Coming Soon | [Download](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/calibration/cps_week_test_cases_2-24_camera_calibration.json)
| Test 19 | Coming Soon |  [Download](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-19/cps-test-19-all.archive?authuser=1) | Coming Soon | [Download](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/calibration/cps_week_test_cases_2-24_camera_calibration.json)
| Test 20 | Coming Soon |  [Download](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-20/cps-test-20-all.archive?authuser=1) | Coming Soon | [Download](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/calibration/cps_week_test_cases_2-24_camera_calibration.json)
| Test 21 | Coming Soon |  [Download](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-21/cps-test-21-all.archive?authuser=1) | Coming Soon | [Download](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/calibration/cps_week_test_cases_2-24_camera_calibration.json)
| Test 22 | Coming Soon |  [Download](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-22/cps-test-22-all.archive?authuser=1) | Coming Soon | [Download](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/calibration/cps_week_test_cases_2-24_camera_calibration.json)
| Test 23 | Coming Soon |  [Download](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-23/cps-test-23-all.archive?authuser=1) | Coming Soon | [Download](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/calibration/cps_week_test_cases_2-24_camera_calibration.json)
| Test 24 | Coming Soon |  [Download](https://storage.cloud.google.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-24/cps-test-24-all.archive?authuser=1) | Coming Soon | [Download](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/calibration/cps_week_test_cases_2-24_camera_calibration.json)

## Getting Started

### Obtain a competitor token
After submitting your abstract describing your approach you will receive a competitor token.
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
git clone https://github.com/JoaoDiogoFalcao/AutoCheckout.git
cd AutoCheckout/
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

### Sensor Data Questions
####  What is the sample rate?
The sensor data is sampled at 60Hz. Each message contains a batch of 12 samples.

####  What is the noise level?
The noise level varies highly from testcase to testcase and from shelf to shelf due to environmental factors such as nearby vibrations and electrical noise.

#### What is the max weight?
The sensors are rated for 20kg per plate.

#### Do I need to account for sensor nonlinearity?
No. The nonlinearity error is orders of magnitude below the baseline noise from the environment.

#### Are the absolute weight values reliable?
No. The absolute weight measured by the sensors is not zeroed and may drift over long periods of time (hours or days). Relatively changes, however, are reliable.
