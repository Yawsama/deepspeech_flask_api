from subprocess import Popen
import os
import requests
import zlib
import json
import shutil

class AudioFile():
	def __init__ (self, uuid):
		self.dest_folder = "./public/audio_assets/"
		self.uuid = uuid

	# Downloads audio from URL and inserts in directory
	def post_audio(self, url):
		status_code = 201
		if not os.path.exists(self.dest_folder):
			os.makedirs(self.dest_folder)
		bytes_url = bytes(url, 'utf-8')	
		self.uuid = str(zlib.crc32(bytes_url))
		if os.path.exists(self.dest_folder + self.uuid):
			status_code = 409
		else:
			os.makedirs(self.dest_folder + self.uuid)
			filename = url.split('/')[-1].replace(" ", "_")	
			file_path = os.path.join(self.dest_folder, self.uuid, filename)
			r = requests.get(url, stream=True)
			if r.ok:
				print("saving to", os.path.abspath(file_path))
				with open(file_path, 'wb') as f:
					for chunk in r.iter_content(chunk_size=1024 * 8):
						if chunk:
							f.write(chunk)
							f.flush()
							os.fsync(f.fileno())
						else:
							status_code = 408
			else:
				status_code = 404
		return self.uuid, status_code

	# Runs deepspeech on audio files
	def generate_transcript(self):
		status_code = 404
		if(self.uuid=="run_all"):
			if os.path.exists(self.dest_folder):
				for d in os.scandir(self.dest_folder):
					for f in os.scandir(d):
						if (f.path.endswith(".wav") and (len(os.listdir(d))<3)):
							self.run_deepspeech(d.path, f.path)
							status_code = 201
						else:
							status_code = 409
		uuid_folder_path = os.path.join(self.dest_folder, self.uuid) 
		if os.path.exists(uuid_folder_path):
			for f in os.scandir(uuid_folder_path):
				if (f.path.endswith(".wav") and (len(os.listdir(uuid_folder_path))<3)):
					self.run_deepspeech(uuid_folder_path, f.path)
					status_code = 201
				else:
					status_code = 409
		return status_code

	# Deepspeech process helper method
	def run_deepspeech(self, uuid_folder_path, file_path):
		output_path = os.path.abspath(os.path.join(uuid_folder_path, "out.json"))
		run_output_path = os.path.abspath(os.path.join(uuid_folder_path, "run_output.txt"))
		dsr_script_path = os.path.abspath("./public/dspeechScript.sh")
		log = open(run_output_path, 'a')
		dsr_process = Popen([dsr_script_path, file_path, output_path], stdout=log, stderr=log)
		dsr_process.wait()

	# Retrieves transcript from out.json
	def get_transcript(self):
		status_code = 404
		format_t_file = {}
		uuid_folder_path = os.path.join(self.dest_folder, self.uuid) 

		if os.path.exists(uuid_folder_path):
			for f in os.scandir(uuid_folder_path):
				if f.path.endswith(".json"):
					with open(f.path) as t_file:
						t_file = json.load(t_file)
					for i in t_file['transcripts']:
						format_t_file.update(i)
					status_code = 201
		return format_t_file, status_code

	# Deletes audio file's folder and its conntents
	def delete_audio(self):
		status_code = 409
		if(self.uuid=="delete_all"):
			shutil.rmtree(self.dest_folder)
			os.mkdir(self.dest_folder)
			status_code = 204
		else:
			total_path = self.dest_folder + self.uuid
			if os.path.exists(total_path):
				shutil.rmtree(total_path)
				status_code = 204
		return status_code








