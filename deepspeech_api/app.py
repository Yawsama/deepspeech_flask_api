from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort
from audio_file import AudioFile

app = Flask(__name__)
api = Api(app)

audio_post_args = reqparse.RequestParser()
audio_post_args.add_argument("URL", type=str, help="A URL containing the WAV audio file is required...", required=True)

class SpeechToText(Resource):
    def post(self, uuid):
        args = audio_post_args.parse_args()
        audioURL = args.get("URL")
        provisioner = AudioFile(uuid)
        uuidFile, status_code = provisioner.post_audio(audioURL)
        if status_code==409:
            abort(status_code, message="This audio file already exists...")
        if status_code==408:
            abort(status_code, message="The audio file from this URL could not be processed...")
        if status_code==404:
            abort(status_code, message="This is not a valid URL...")
        return {"UUID" : uuidFile}, status_code

    def put(self, uuid):
        provisioner = AudioFile(uuid)
        status_code = provisioner.generate_transcript()
        if status_code==404:
            abort(status_code, message="This UUID does not exist...")
        if status_code==409:
            abort(status_code, message="This audio file has already been processed...")
        if(uuid=="run_all"):
            message = "All audio files have been transcribed"
        else:
            message = uuid + "'s audio file has been transcribed"
        return {"SUCCESS" : message}, 201

    def get(self, uuid):
        provisioner = AudioFile(uuid)
        transcript, status_code = provisioner.get_transcript() 
        if status_code==404:
            abort(status_code, message="Need to generate transcript for audio file. Use PUT with UUID to generate...")
        return transcript, status_code

    def delete(self, uuid):
        provisioner = AudioFile(uuid)
        status_code = provisioner.delete_audio()
        if status_code==409:
            abort(status_code, message="This file does not exist...")
        return status_code


api.add_resource(SpeechToText, "/audiofile/<string:uuid>")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
