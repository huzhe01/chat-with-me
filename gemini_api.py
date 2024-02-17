import pathlib
import textwrap

import google.generativeai as genai

import requests
import json
YOUR_API_KEY = 'AIzaSyAbP0mbJUbWTqKyeRRrSngfkIUPSRWMDgI'
url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + YOUR_API_KEY
headers = {'Content-Type': 'application/json'}
data = {
  "contents": [
    {
      "parts": [
        {
          "text": "Write a story about a magic backpack"
        }
      ]
    }
  ]
}

response = requests.post(url, headers=headers, data=json.dumps(data))

# print(response.json()['candida'])
response.json()["candidates"][0]["content"]["parts"][0]["text"]