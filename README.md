Code for Implementing an API in Python

Disclaimer: This code is based on [blog post about creating a flask-mysql app with docker](https://stavshamir.github.io/python/dockerizing-a-flask-mysql-app-with-docker-compose/)

## Pre-requisites
You will need to [Docker-compose](https://docs.docker.com/compose/install/) to run this code.
Also for testing, you will need [Postman](https://www.postman.com/downloads/) or a different tool.


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


## Additional Improvements
I used a simple OpenCV processing function to extract meta-data from the video because I wanted to finish this task quickly. Using a machine learning model would be more beneficial, as they provide semantically more relevant information. The challenge is not in running a model in inference mode, but running the model in a manner that provides useful information.

Let's say we are using [Mask-Track-RCNN](https://github.com/youtubevos/MaskTrackRCNN). If we provide this model with a video in inference mode, it will probably give us a list of objects and their locations in a given frame. But this information in its raw format is probably not useful, because of its sheer volume. Aggregating this information is not intuitive, because each video might consist of multiple `scenes` with different topics. An object might not be visible in future frames because it wandered outside of the camera range or a scene transition happened.

The idea of a video consisting as a series of `scenes` is paramount to the way absorb videos as humans and our data model should reflect this. Knowing this, a more prudent approach is not to run the model on the entire video, but to run it on individual scenes. We can do this using the [PySceneDetect](https://github.com/Breakthrough/PySceneDetect) framework. At this point we can aggregate the information for the type and location of objects in a given scene accordingly. For example, we can extract the start and end location of moving objects (e.g., people) for a given scene.

The code is woefully under-tested. More tests need to be added for coverage. For unit-testing the database, I need to perform mocking, this can be added with more time.

Ideally tests should be run automatically on `Travis` following each repo push.
