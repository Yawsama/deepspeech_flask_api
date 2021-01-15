import requests

BASE = "http://127.0.0.1:5000/"

# Adding an audio file
response = requests.post(BASE + "/audiofile/post", {"URL": "https://uweb.engr.arizona.edu/~429rns/audiofiles/cutafew.wav"})
print(response.json())
input()

# Running deepspeech
response2 = requests.put(BASE + "/audiofile/335944824")
print(response2.json())
input()

# Gettinng transcript
response3 = requests.get(BASE + "/audiofile/335944824")
print(response3.json())
input()

# Deleting audio file and transcript
response4 = requests.delete(BASE + "/audiofile/335944824")
print(response4.json())
input()

# Adding two audio files
response5 = requests.post(BASE + "/audiofile/post", {"URL": "https://uweb.engr.arizona.edu/~429rns/audiofiles/cutafew.wav"})
print(response5.json())
input()
response6 = requests.post(BASE + "/audiofile/post", {"URL": "https://uweb.engr.arizona.edu/~429rns/audiofiles/howsoon.wav"})
print(response6.json())
input()

# Running deepspeech on all available audio files
response7 = requests.put(BASE + "/audiofile/run_all")
print(response7.json())
input()

# Getting both transcripts
response8 = requests.get(BASE + "/audiofile/335944824")
print(response8.json())
input()
response9 = requests.get(BASE + "/audiofile/1498092488")
print(response9.json())
input()

# Deleting all available audio files and transcripts 
response10 = requests.delete(BASE + "/audiofile/delete_all")
print(response10.json())
input()