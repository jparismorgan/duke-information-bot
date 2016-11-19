from flask import Flask, request
import requests
import json
import traceback
import random
app = Flask(__name__)

token = "EAATFD6LxlrkBAASD6ZAjgZBJ8e3pyi6aEjdV9hxAAygrUwtgMTvixTCRXh5yMQ87XoHZAizv2KtBR7iGvGER8cpKZAZBGSIr1thRFBKpwJDX6wXI5es7ThJQnNnZBNwZBqZBVwASWk8iX5N2xZAFCvwtF7U2pkebxdWYBjhiKFylTBAZDZD"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
  if request.method == 'POST':
    try:
      data = json.loads(request.data)
      text = data['entry'][0]['messaging'][0]['message']['text'] # Incoming Message Text
      sender = data['entry'][0]['messaging'][0]['sender']['id'] # Sender ID
      payload = {'recipient': {'id': sender}, 'message': {'text': "Hello World"}} # We're going to send this back
      r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload) # Lets send it
    except Exception as e:
      print traceback.format_exc() # something went wrong
  elif request.method == 'GET': # For the initial verification
    if request.args.get('hub.verify_token') == '<VERIFY_TOKEN_HERE>':
      return request.args.get('hub.challenge')
    return "Wrong Verify Token"
  return "Hello Duke" #Not Really Necessary

if __name__ == '__main__':
  app.run(debug=True)