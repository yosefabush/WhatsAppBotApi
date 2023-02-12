import os
import json
import pandas
import requests
import unicodedata
# from Database import Database
from flask import Flask, request
from requests.structures import CaseInsensitiveDict

app = Flask(__name__)

token = os.getenv('TOKEN')
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PHONE_NUMBER_ID_PROVIDER = os.getenv("NUMBER_ID_PROVIDER")
WHATS_API_URL = 'https://api.whatsapp.com/v3'
FACEBOOK_API_URL = 'https://graph.facebook.com/v15.0'
# db = Database()
to = None
language_support = {"he": "he_IL", "en": "en_US"}

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Authorization"] = f"Bearer {token}"


@app.route("/")
def whatsapp_echo():
    return "WhatsApp bot server is ready1!"


@app.route("/bot", methods=["POST", "GET"])
def receive_message():
    """Receive a message using the WhatsApp Business API."""
    global to
    try:
        if request.method == "GET":
            mode = request.args.get("hub.mode")
            challenge = request.args.get("hub.challenge")
            received_token = request.args.get("hub.verify_token")
            if mode and received_token:
                if mode == "subscribe" and received_token == VERIFY_TOKEN:
                    return challenge, 200
                else:
                    return "", 403
        else:
            try:
                # receive data from whatsapp webhooks
                user_msg = request.values.get('Body', '').lower()
                to = request.values.get('From', '').lower()
                to = to.split("+")[1]
                print("receive data from whatsapp webhooks", user_msg, to)
            except:
                # receive data from postman
                data = request.get_json()
                to = data['to']
                user_msg = data['template']['name']
                print("receive data from postman", user_msg, to)

            # Do something with the received message
            print("Received message:", user_msg)

            _language = "en" if 'HEBREW' not in unicodedata.name(user_msg.strip()[0]) else "he"
            print(_language)
            if _language == "en":
                if 'hello' in user_msg:
                    print(send_response_using_whatsapp_api('Hi There!'))
                elif 'where' in user_msg:
                    print(send_response_using_whatsapp_api("Go to: http://google.com"))
                else:
                    print(send_response_using_whatsapp_api("Unknown msg"))
            else:
                if 'היי' in user_msg:
                    print(send_response_using_whatsapp_api("שלום רב!"))
                else:
                    print(send_response_using_whatsapp_api("אני לומד להציק ללידור הגיי"))
            return str("Done")
    except Exception as ex:
        return f"Something went wrong : '{ex}'"


def send_response_using_whatsapp_api(message):
    """Send a message using the WhatsApp Business API."""
    try:
        print(f"Sending response for f{message}")
        url = f"{FACEBOOK_API_URL}/{PHONE_NUMBER_ID_PROVIDER}/messages"
        url = f"{WHATS_API_URL}/messages?token={token}"
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": f"{to}",
            "type": "text",
            "text": {
                "preview_url": False,
                "body": f"{message}"
            }
        }

        pay = {
            "messaging_product": "whatsapp",
            "to": f"{to}",
            "type": "template",
            "template": {
                "name": "hello_world",
                "language": {
                    "code": "en_US"
                }
            }
        }

        response = requests.post(url, json=payload, headers=headers, verify=False)
        if not response.ok:
            return f"Failed to send message, json : '{payload}'\nresponse: '{response}'"
        return f"Message sent successfully to :'{to}'!"
    except Exception as EX:
        return f"Error send response : '{EX}'"


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=5000)
