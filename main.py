"""`main` is the top level module for your Flask application."""
import os
import sys
from wit import Wit
import json
import logging
import json
import action_processor

# Import the Flask Framework
from flask import Flask, request
# import process

from google.appengine.api import urlfetch
import MySQLdb
import webapp2

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

CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')

def connect_to_cloudsql():
    # When deployed to App Engine, the `SERVER_SOFTWARE` environment variable
    # will be set to 'Google App Engine/version'.
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        # Connect using the unix socket located at
        # /cloudsql/cloudsql-connection-name.
        cloudsql_unix_socket = os.path.join(
            '/cloudsql', CLOUDSQL_CONNECTION_NAME)

        db = MySQLdb.connect(
            unix_socket=cloudsql_unix_socket,
            user=CLOUDSQL_USER,
            passwd=CLOUDSQL_PASSWORD)

    # If the unix socket is unavailable, then try to connect using TCP. This
    # will work if you're running a local MySQL server or using the Cloud SQL
    # proxy, for example:
    #
    #   $ cloud_sql_proxy -instances=your-connection-name=tcp:3306
    #
    else:
        db = MySQLdb.connect(
            host='127.0.0.1', user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD)

    return db

class Main(webapp2.RequestHandler):
    def get(self):
        """Simple request handler that shows all of the MySQL variables."""
        self.response.headers['Content-Type'] = 'text/plain'

        db = connect_to_cloudsql()
        cursor = db.cursor()
        cursor.execute('SHOW VARIABLES')

        for r in cursor.fetchall():
            self.response.write('{}\n'.format(r))

app2 = webapp2.WSGIApplication([
    ('/', Main),
], debug=True)

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

def send(request, response):
    # fb_id as session_id
    fb_id = request['session_id']
    text = response['text']
    # send message
    send_fb_message(fb_id, text)

# def messaging_events(payload):
#   """Generate tuples of (sender_id, message_text) from the
#   provided payload.
#   """
#   data = json.loads(payload)
#   messaging_events = data["entry"][0]["messaging"]
#   for event in messaging_events:
#     if "message" in event and "text" in event["message"]:
#       yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
#     else:
#       yield event["sender"]["id"], "I'm sorry, there was an error processing your request. source: messaging_events()"
#
# @app.route('/', methods=['POST'])
# def webhook():
#     """Return a friendly HTTP greeting."""
#     data = request.get_json()
#     for sender, message in messaging_events(data):
#         #do something with sender and message
#         send_fb_message(sender, message)
#     return "ok"
#
#     # always return 200 to Facebook's original POST request so they know you handled their request
#    # process.messenger_post(request)
#     return "OK", 200
#     #435ab3e9281b9256d2beb3125b71dd01e9a85af6

@app.route('/', methods=['POST'])
def webhook():
    """Return a friendly HTTP greeting."""
    data = request.get_json()
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']
    send_fb_message(sender, message[::-1])
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

actions = {}

# Setup Wit Client
client = Wit(access_token=WIT_TOKEN, actions=actions)