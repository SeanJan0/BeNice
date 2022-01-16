import pyaudio
import websockets
import asyncio
import base64
import json
import openai
from config import auth_key_assembly, auth_key_open

import streamlit as st

openai.api_key = auth_key_open

if 'recording' not in st.session_state:
    st.session_state['recording'] = False

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()
 
# starts recording
stream = p.open(
   format=FORMAT,
   channels=CHANNELS,
   rate=RATE,
   input=True,
   frames_per_buffer=FRAMES_PER_BUFFER
)

def toggle_on():
    st.session_state['recording'] = True
    print("record")
    
def toggle_off():
    st.session_state['recording'] = False
    print("mute")

st.title("Recommender")

start_record, stop_record = st.columns(2)

statement = st.empty()

option_1, option_2, option_3 = st.columns(3)
option_1 = st.empty()
option_2 = st.empty()
option_3 = st.empty()

start_record.button("Listen", help="Turn on listening", on_click=toggle_on)
stop_record.button("Stop Listening", help="Stop listening", on_click=toggle_off)

# the AssemblyAI endpoint we're going to hit
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

async def send_receive(statement, option_1, option_2, option_3):
   print(f'Connecting websocket to url ${URL}')
   async with websockets.connect(
       URL,
       extra_headers=(("Authorization", auth_key_assembly),),
       ping_interval=5,
       ping_timeout=20
   ) as _ws:
       r = await asyncio.sleep(0.1)
       print("Receiving SessionBegins ...")
       session_begins = await _ws.recv()
       print(session_begins)
       print("Sending messages ...")
       async def send():
           while st.session_state['recording']:
               try:
                   data = stream.read(FRAMES_PER_BUFFER)
                   data = base64.b64encode(data).decode("utf-8")
                   json_data = json.dumps({"audio_data":str(data)})
                   r = await _ws.send(json_data)
               except websockets.exceptions.ConnectionClosedError as e:
                   print(e)
                   assert e.code == 4008
                   break
               except Exception as e:
                   assert False, "Not a websocket 4008 error"
               r = await asyncio.sleep(0.01)
          
           return True
      
       async def receive():
           curr_prompt = ""
           gpt_ran = False
           while st.session_state['recording']:
               try:
                   result_str = await _ws.recv()
                   if json.loads(result_str)['message_type'] == 'FinalTranscript':
                       print(json.loads(result_str)['text'])
                       statement.empty()
                       with statement.container():
                          st.header(json.loads(result_str)['text'])
                       gpt_ran = True
                       curr_prompt = "Him: " + json.loads(result_str)['text']
                       response = openai.Completion.create(
                        engine="davinci",
                        prompt=curr_prompt,
                        temperature=0.7,
                        max_tokens=30,
                        top_p=1,
                        n=3,
                        frequency_penalty=0.0,
                        presence_penalty=0.0,
                        stop=["Him: "]
                        )

                       option_1.empty()
                       answer1 = response.choices[0].text
                       option_1.text(answer1.split(': ')[-1])

                       option_2.empty()
                       answer2 = response.choices[1].text
                       option_2.text(answer2.split(': ')[-1])
                       
                       option_3.empty()
                       answer3 = response.choices[2].text
                       option_3.text(answer3.split(': ')[-1])
                       
                       
                
                    

                       
               except websockets.exceptions.ConnectionClosedError as e:
                   print(e)
                   assert e.code == 4008
                   break
               except Exception as e:
                   assert False, "Not a websocket 4008 error"
      
       send_result, receive_result = await asyncio.gather(send(), receive())

asyncio.run(send_receive(statement, option_1, option_2, option_3))