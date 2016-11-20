"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask, request

import requests


#Will this work?

app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

FACEBOOK_APP_ID = ""
FACEBOOK_APP_SECRET = ""
FACEBOOK_PAGE_ID = ""
FACEBOOK_PAGE_ACCESS_TOKEN = ""
FACEBOOK_WEBHOOK_VERIFY_TOKEN = "EAATFD6LxlrkBAOzI1q6EcKHKarcirRL08nl9wApgBXmJyVxndZBpjR7ZA72frJS89qcOlPkoOZAGEhqSgxRPamAdaynCnZCicGZC67ZBAYfw96CRbUS5bRSd8pXqOuCyzqD6ejg4VHMoLTrIZCdhGHS4101ZChhtUEh1p4cGIQfZBeQZDZD"
FACEBOOK_BOT_NAME = ""


@app.route('/', methods=['POST'])
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


@app.route('/webhook')
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == FACEBOOK_WEBHOOK_VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
