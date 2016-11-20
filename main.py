"""`main` is the top level module for your Flask application."""
import os
import sys
from wit import Wit
import json
import logging
import json
import RestaurantScraper

# Import the Flask Framework
from flask import Flask, request
# import process
import action_processor

from google.appengine.api import urlfetch
# from googleapiclient.discovery import build
# from oauth2client.client import GoogleCredentials

app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

WIT_TOKEN = 'SSMXAOJXF2MR2LWBEGCMFAWJ7WSSFOEC'
FACEBOOK_APP_ID = ""
FACEBOOK_APP_SECRET = ""
FACEBOOK_PAGE_ID = ""
FACEBOOK_PAGE_ACCESS_TOKEN = "EAATFD6LxlrkBAHcZBCsZAiCV1lZAbWisuudFNhmOscxRPSUUUFHVoWbDm8rxf4tiUf0YyKccPkteMjbEuVsIKlQzwZAqpUFMn2NqWdU0KDnyDt1kfNnHTlpMDZCEIvczukaQFlopgiuMvSB0MkmsPqiO6v4lZABZBwAH19VWZCtg1wZDZD"
FACEBOOK_WEBHOOK_VERIFY_TOKEN = "secret"
FACEBOOK_BOT_NAME = ""

def send_fb_message(user_id, msg):
    """sends message 'msg' to user 'user_id'"""
    payload = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    try:
        req = urlfetch.fetch(
            'https://graph.facebook.com/v2.6/me/messages?access_token=' + FACEBOOK_PAGE_ACCESS_TOKEN,
            json.dumps(payload),
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
    # send_fb_message(sender, message[::-1])
    client.run_actions(session_id=sender, message=message)
    # always return 200 to Facebook's original POST request so they know you handled their request
    return "OK", 200

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

def send(request, response):
    """
    Sender function
    """

    # We use the fb_id as equal to session_id
    fb_id = request['session_id']
    text = response['text']
    # send message
    logging.info(text)
    send_fb_message(fb_id, text)


def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val

@app.route('/update')
def test():
    print 'updating'
    RestaurantScraper.get_restaurants()


actions = {'send': send,
           'createEvent': action_processor.dukeSearch,
           'findEvent': action_processor.dukeSearch,
           'find_location_of': action_processor.find_location_of,
           'dukeSearch': action_processor.dukeSearch,
           'getBusTimes': action_processor.getBusTimes,
           }

# Setup Wit Client
client = Wit(access_token=WIT_TOKEN, actions=actions)

# # Setup Google Cloud Datastore
#
# credentials = GoogleCredentials.get_application_default()
# service = build('compute', 'v1', credentials=credentials)
#
# PROJECT = 'duke-information-bot'
# ZONE = 'us-east1-a'
# request = service.instances().list(project=PROJECT, zone=ZONE)
# response = request.execute()

