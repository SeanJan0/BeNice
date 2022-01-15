import requests
import openai
from config import auth_key_open

# Load your API key from an environment variable or secret management service
openai.api_key = auth_key_open

prompt = input('Her: ')

response = openai.Completion.create(
  engine="davinci",
  prompt=prompt,
  temperature=0.6,
  max_tokens=30,
  top_p=1,
  n = 4,
  frequency_penalty=0.0,
  presence_penalty=0.0,
  stop=["Her: "]
)
for i in range(4):
    print(prompt, response.choices[i].text)
