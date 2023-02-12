import os
import json
import pandas
import requests
import unicodedata
from flask import Flask
from flask import request
# from Database import Database
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

IS_FIRST_MESSAGE = True
app = Flask(__name__)
# db = Database()
WHATS_APP = 'https://api.whatsapp.com/v3'
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
to = None
my_number = "+14155238886"  # "+15550398859"
dest_number = "+972525899132"


@app.route("/")
def whatsapp_echo():
    global IS_FIRST_MESSAGE
    if IS_FIRST_MESSAGE:
        IS_FIRST_MESSAGE = False
        send_message_through_twilio(my_number, dest_number)
        return "WhatsApp HTTP API start"
    return "WhatsApp HTTP API Echo server is ready!"


@app.route("/bot", methods=["POST"])
def whatsapp_webhook():
    global IS_FIRST_MESSAGE
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        challenge = request.args.get("hub.challenge")
        received_token = request.args.get("hub.verify_token")

        if mode and received_token:
            if mode == "subscribe" and received_token == VERIFY_TOKEN:
                return challenge, 200
            else:
                return "", 403
        if IS_FIRST_MESSAGE:
            IS_FIRST_MESSAGE = False
            send_message_through_twilio(my_number, dest_number)
            return "WhatsApp HTTP API start from webhook"
    user_msg = request.values.get('Body', '').lower()
    bot_resp = MessagingResponse()
    msg = bot_resp.message()
    is_eng_language = True if 'HEBREW' not in unicodedata.name(user_msg.strip()[0]) else False
    if is_eng_language:
        if 'hello' in user_msg:
            msg.body('Hi There!')
        elif 'where' in user_msg:
            msg.body("Go to: http://google.com")
        else:
            msg.body("Unknown msg")
    else:
        if 'היי' in user_msg:
            msg.body("שלום רב!")
        else:
            msg.body("אני לומד להציק ללידור הגיי")
    return str(bot_resp)


def receive_message(token):
    """Receive a message using the WhatsApp Business API."""
    global to
    url = f"{WHATS_APP}/messages?token={token}"

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Failed to receive message")

    messages = response.json()
    if not messages:
        return None

    to = messages[0]["from"]


def send_message_using_whatsapp_api(token, message):
    """Send a message using the WhatsApp Business API."""
    url = f"{WHATS_APP}/messages?token={token}"

    payload = {
        "to": receive_message(token),
        "message": message
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception("Failed to send message")


def send_message_through_twilio(_from, to):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body='Hello there!',
        from_=f'whatsapp:{_from}',
        to=f'whatsapp:{to}'
    )

    print(message.sid)
    return message.sid


def send_message_using_facebook():
    url = "https://graph.facebook.com/v15.0/100380176318714/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": "972525899132",
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {
                "code": "en_US"
            }
        }
    }
    result = requests.post(url, json=payload, verify=False)
    if result.status_code != 200:
        raise Exception("Failed to send message")


@app.route('/get_users', methods=['GET'])
def get_users():
    try:
        pass
        # return json.dumps(db.execute_query("SELECT callInfo FROM seda.ic_call_info where seda.ic_call_info.cli='sipmsg';"))
    except Exception as ex:
        return f"error: {ex}"


if __name__ == "__main__":
    app.run(debug=True)
    # "ngrok.exe http 5000"
    # app.run(host='0.0.0.0', port=5000)
