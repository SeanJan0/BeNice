import requests
import os
import sys
from config import auth_key

os.chdir(os.path.dirname(sys.argv[0]))

headers = {
    "authorization": auth_key,
    "content-type": "application/json"
}

def read_file(filename):
   with open(filename, 'rb') as _file:
       while True:
           data = _file.read(5242880)
           if not data:
               break
           yield data
 
upload_response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers, data=read_file('bgb.mp3'))
audio_url = upload_response.json()['upload_url']

transcript_request = {'audio_url': audio_url}
endpoint = "https://api.assemblyai.com/v2/transcript"
transcript_response = requests.post(endpoint, json=transcript_request, headers=headers)
_id = transcript_response.json()['id']

endpoint = "https://api.assemblyai.com/v2/transcript/" + _id
polling_response = requests.get(endpoint, headers=headers)


while polling_response.json()['status'] != 'completed':
   polling_response = requests.get(endpoint, headers=headers)
   print("1")
else:
   with open(_id + '.txt', 'w') as f:
       f.write(polling_response.json()['text'])
   print('Transcript saved to', _id, '.txt')