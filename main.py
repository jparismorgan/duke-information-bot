"""`main` is the top level module for your Flask application."""
import os
import sys
import json
import logging

# Import the Flask Framework
from flask import Flask, request
import process

from google.appengine.api import urlfetch

app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

FACEBOOK_APP_ID = ""
FACEBOOK_APP_SECRET = ""
FACEBOOK_PAGE_ID = ""
FACEBOOK_PAGE_ACCESS_TOKEN = "EAATFD6LxlrkBAHcZBCsZAiCV1lZAbWisuudFNhmOscxRPSUUUFHVoWbDm8rxf4tiUf0YyKccPkteMjbEuVsIKlQzwZAqpUFMn2NqWdU0KDnyDt1kfNnHTlpMDZCEIvczukaQFlopgiuMvSB0MkmsPqiO6v4lZABZBwAH19VWZCtg1wZDZD"
FACEBOOK_WEBHOOK_VERIFY_TOKEN = "secret"
FACEBOOK_BOT_NAME = ""

#old method
def reply(user_id, msg):
    """Sends the message to usr_id. """
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + FACEBOOK_PAGE_ACCESS_TOKEN, json=data)

    # handle the response to the subrequest you made
    if not resp.ok:
        # log some useful info for yourself, for debugging
        print 'jeepers. %s: %s' % (fb_response.status_code, fb_response.text)

    print(resp.content)


#new method for google cloud
def send_fb_message(user_id, msg):
    payload = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    try:
        req = urlfetch.fetch(
            'https://graph.facebook.com/v2.6/me/messages?access_token=' + FACEBOOK_PAGE_ACCESS_TOKEN,
            payload,
            urlfetch.POST,
            {'Content-Type': 'application/json'}
        )
        logging.debug(req.content)
    except urlfetch.Error as e:
        logging.error(e.message)

@app.route('/', methods=['POST'])
def webhook():
    """Return a friendly HTTP greeting."""
    data = request.get_json()
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']
    reply(sender, message[::-1])

    # always return 200 to Facebook's original POST request so they know you
    # handled their request

   # process.messenger_post(request)
    return "OK", 200
    #435ab3e9281b9256d2beb3125b71dd01e9a85af6


@app.route('/', methods=['GET'])
def verify():
    #when the endpoint is registered as a webhook, it must echo back
    #the 'hub.challenge' value it receives in the query arguments
    if (3==3): #request.args.get('hub.verify_token', '') == FACEBOOK_WEBHOOK_VERIFY_TOKEN:
        return request.args.get('hub.challenge', '')
    else:
        return 'Error, wrong validation token'

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
