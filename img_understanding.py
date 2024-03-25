import os
from dotenv import load_dotenv
import cv2
import re
import json
import base64
import requests

load_dotenv()

def resize(img, max_length=512):
  h, w, c = img.shape
  if max(h, w) > max_length:
    if h > w:
      w = int(w * max_length / h)
      h = max_length
    else:
      h = int(h * max_length / w)
      w = max_length
  return cv2.resize(img, (w, h))

def encode_image(img):
  _, enc_data = cv2.imencode('.jpg', img)
  base64_image = base64.b64encode(enc_data).decode('utf-8')
  return base64_image
  
def get_image_info(img):
  img_resize = resize(img)
  base64_image = encode_image(img_resize)
  
  prompt = """Tell me the title and the painter of the picture in JSON format.
  If you don't know the picture, please return empty data in JSON format. 
  
  Here is an example.
  {
    "title": "AB",
    "painter": "CD"
  }
  """
  
  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"
  }
  
  payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": prompt
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}"
            }
          }
        ]
      }
    ],
    "max_tokens": 100
  }
  
  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
  data = response.json()['choices'][0]["message"]["content"]
  
  # jsonデータの取り出し
  pattern = r"```json([^`]+)"
  match = re.search(pattern, data)
  if match is None:
    print(data)
    return "", ""
  json_str = match.group(1)
  json_data = json.loads(json_str)
  
  # 作品名と画家名の抽出
  title = json_data.get("title", "")
  painter = json_data.get("painter", "")
  print(title, painter)
  return title, painter

def get_caption_from_img(img):
  img_resize = resize(img)
  base64_image = encode_image(img_resize)
  
  prompt ="""Explain briefly about the art techniques and its effects in the picture by mentioning where in the picture each technique is used.  
  The answer should be sentences, not in bullet points."""
  
  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"
  }
  
  payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": prompt
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}"
            }
          }
        ]
      }
    ],
    "max_tokens": 200
  }
  
  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
  caption = response.json()['choices'][0]["message"]["content"]
  return caption