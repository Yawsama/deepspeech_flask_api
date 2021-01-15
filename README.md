# DeepSpeech REST API 

## Overview
This is a REST microservice created using Flask that streamlines the [Skimo Speech-To-Text Service](https://github.com/skimotv/SkimoSpeechToTextService/) and is based on the open source engine [DeepSpeech](https://github.com/mozilla/DeepSpeech). The API accepts a WAV file in the POST request and returns a full JSON transcript with timecodes in the GET   

## Installing DeepSpeech
This service utilizes **DeepSpeech Version 0.9.2**

Full instructions for downloading and installing DeepSpeech can be found [here](https://deepspeech.readthedocs.io/en/v0.9.2/)

For development purposes, the path to the DeepSpeech models can be adjusted through the shell script found in `public/dspeechScript.sh` 

## Usage
This REST API provides four request methods.

### POST
Used to download an audio file from an URL source, generate a UUID, and place each file into the `public/audio_assets` directory. Uses the `/audiofile/post` endpoint along with a JSON in the body containing the URL. Specific format can be found in `test.py`.

### PUT
Used to run the DeepSpeech conversion on audio files. Uses the `/audiofile/<uuid>` endpoint to process a single audio file or `/audiofile/run_all` to process all audio files.

### GET
Used to retrieve a JSON transcript with timecodes. Uses the `/audiofile/<uuid>` to specify an audio file.

### DELETE
Used to delete an audio file along with its transcript. Uses the `/audiofile/<uuid>` endpoint to specify a single audio file or the `/audiofile/delete_all` endpoint to delete all audio files and transcripts. 

