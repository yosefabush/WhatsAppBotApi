import os
import unicodedata
from flask import Flask
from flask import request
import requests
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
IS_FIRST_MESSAGE = True


@app.route("/")
def whatsapp_echo():
    global IS_FIRST_MESSAGE
    if IS_FIRST_MESSAGE:
        IS_FIRST_MESSAGE = False
        # sms("+14155238886", "+972525899132")
        sms("+15550398859", "+972525899132")
        return "WhatsApp HTTP API start"
    return "WhatsApp HTTP API Echo server is ready!"


@app.route("/bot", methods=["POST"])
def whatsapp_webhook():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "YOURVARIFICATIONTOKEN":
            return "Verification token missmatch", 403
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


# @app.route("/test", methods=["GET"])
def sms(_from, to):
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
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


def send_message():
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

    pass


@app.route('/receive_msg', methods=['POST', 'GET'])
def webhook():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "YOUR VARIFICATION TOKEN":
            return "Verification token missmatch", 403
        return request.args['hub.challenge'], 200
    return "Hello world", 200


if __name__ == "__main__":
    app.run(debug=True)
