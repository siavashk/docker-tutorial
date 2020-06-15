Code for Implementing an API in Python

Disclaimer: This code is based on [blog post about creating a flask-mysql app with docker](https://stavshamir.github.io/python/dockerizing-a-flask-mysql-app-with-docker-compose/)

## Pre-requisites
You will need to [Docker-compose](https://docs.docker.com/compose/install/) to run this code.
Also for testing the API, you will need [Postman](https://www.postman.com/downloads/) or a different tool for API testing.


## Installation
Simply run:
```bash
docker-compose up
```

This should start the server at `0.0.0.0:5000`.

## Usage
I have provided two API end-points. The first one is a `POST` request that supplies a video for the server to process. The server will process this file using `Opencv` extracts the `video_name`, `height`, `width`, `frames_per_second`, `frame_count` for the given video. Additionally, I store this information with a timestamp in a relational database for logging purposes. The endpoint is available under `http://0.0.0.0:5000/video`.

Follow the instructions as displayed in ![Post request](/instructions.png "Figure 1: Instructions for submitting a POST request")<br/>

Make sure you set the request type as `POST` and use the correct end-point as highlighted in the green rectangle. Next, navigate to the `Body` section and add a `(key, value)` pair for the form-data. Choose a video file with a `.mp4` extension as highlighted in the red rectangle. Finally, hit the blue `Send` button and you should see a similar response from the server as highlighted with the blue rectangle.

I have provided the file that I tested along with this repository under `tahm.mp4`.

The second API end-point is only for convenience. It does a `GET` request for the logs and displays it in `JSON` format. I found this to be useful during development. You can try it by navigating to `http://0.0.0.0:5000/logs` in your browser.

## Testing
I used the `pytest` framework for unit testing. I have only added a unit-test for one function, under `app/tests.py`, but more tests can be added given more development time. For now I am installing `pytest` manually using `pip`, and run the tests using:
```bash
cd app && python -m pytest tests.py
```
Ideally tests should be run automatically on `Travis` following each repo push, but that integration can be added later.
