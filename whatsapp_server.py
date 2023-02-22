import os
import json
import pandas
import requests
import unicodedata
from datetime import datetime
# from Database import Database
from flask import Flask, request
from requests.structures import CaseInsensitiveDict
from Models.ConversationSession import ConversationSession

requests.packages.urllib3.disable_warnings()
app = Flask(__name__)

PORT = os.getenv("PORT", default=5000)
TOKEN = os.getenv('TOKEN', default=None)
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", default=None)
PHONE_NUMBER_ID_PROVIDER = os.getenv("NUMBER_ID_PROVIDER", default=None)
FACEBOOK_API_URL = 'https://graph.facebook.com/v16.0'
WHATS_API_URL = 'https://api.whatsapp.com/v3'
TIMEOUT_FOR_OPEN_SESSION_MINUTES = 10
if None in [TOKEN, VERIFY_TOKEN, PHONE_NUMBER_ID_PROVIDER]:
    raise Exception(f"Error on env var '{TOKEN,VERIFY_TOKEN,PHONE_NUMBER_ID_PROVIDER}' ")
# db = Database()
to = None
language_support = {"he": "he_IL", "en": "en_US"}

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Authorization"] = f"Bearer {TOKEN}"

conversation = {
    "Greeting": "Hi I'm ChatBot. Here are the conversation steps to follow:"
}

# Define a list of predefined conversation steps
conversation_steps = {
    "1": "אנא הזן שם משתמש",
    "2": "אנא הזן סיסמא",
    "3": "תודה שפנית אלינו, פרטיך נקלטו במערכת, באיזה נושא נוכל להעניק לך שירות?",
    "4": "אנא הזן קוד מוצר",
    "5": "האם לחזור למספר הסלולרי?",
    "6": "נא רשום בקצרה את תיאור הפנייה",
    "7": "פנייתך התקבלה, נציג טלפוני יחזור אליך בהקדם.",
}

conversation_history = list()
for i in range(5):
    old_session = ConversationSession(f"1234{i}")
    conversation_history.append(old_session)
    if i == 3:
        old_session.call_flow_location = 3

print([item.get_user_id() for item in conversation_history])


@app.route("/")
def whatsapp_echo():
    return "WhatsApp bot server is ready1!"


@app.route("/bot", methods=["POST", "GET"])
def receive_message():
    """Receive a message using the WhatsApp Business API."""
    global to
    print(f"receive_message trigger '{request}'")
    print(f"method '{request.method}'")
    try:
        if request.method == "GET":
            print("Inside GET verify token!")
            # return verify_token(request)
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
                print(f"Inside Post method!")
                print(f"form: '{request.form}' ")
                user_msg = request.values.get('Body', '').lower()
                print(f"user_msg {user_msg}")
                to = request.values.get('From', '').lower()
                print(f"to1 '{to}'")
                # to = to.split("+")[1]
                print(f"to2 '{to}'")
                print(f"values '{request.values}'")
                if '' in [user_msg, to]:
                    print(f"Error on parsing '{request.values}'")
                    raise Exception(f"Empty user msg '{user_msg}' or destination '{to}'")
                print("receive data from whatsapp webhooks", user_msg, to)
            except Exception as ERR:
                # receive data from postman
                print(F"WHATS parse error '{ERR}'")
                try:
                    print(f"postman")
                    data = request.get_json()
                    to = data['to']
                    user_msg = data['template']['name']
                    print("receive data from postman", user_msg, to)
                except Exception as EX:
                    print(f"webhook")
                    webhook()
                    print(f"Fatal Error '{EX}'")
                    raise Exception("Fatal Error")

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


@app.route("/botTest", methods=["POST", "GET"])
def receive_message_new():
    """Receive a message using the WhatsApp Business API."""
    global to
    print(f"receive_message trigger '{request}'")
    print(f"method '{request.method}'")
    try:
        if request.method == "GET":
            print("Inside receive message with verify token")
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
                print(f"Inside Post method")
                user_msg = request.values.get('Body', '').lower()
                print(f"user_msg {user_msg}")
                to = request.values.get('From', '').lower()
                print(f"to1 {to}")
                to = to.split("+")[1]
                print(f"to2 {to}")
                if '' in [user_msg, to]:
                    print(request.get_json())
                    raise Exception("error")
                print("receive data from whatsapp webhooks", user_msg, to)
            except Exception:
                # receive data from postman
                print(f"postman")
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
                chat_whatsapp(user_msg)
                # if 'היי' in user_msg:
                #     print(send_response_using_whatsapp_api("שלום רב!"))
                # else:
                #     print(send_response_using_whatsapp_api("אני לומד להציק ללידור הגיי"))
            return str("Done")
    except Exception as ex:
        return f"Something went wrong : '{ex}'"


# Define a function to handle user input and provide responses
def chat_input():
    # Print a greeting message and the predefined conversation steps
    print(conversation["Greeting"])
    for key, value in conversation_steps.items():
        print(f"{value} - {key}")

    # Get the user's name
    user_id = input(f"{conversation_steps['1']}\n")
    session = None
    conversation_history_ids = [item.get_user_id() for item in conversation_history]
    if user_id in conversation_history_ids:
        session = conversation_history[conversation_history_ids.index(user_id)]
        diff_time = datetime.now() - session.start_data
        seconds_in_day = 24 * 60 * 60
        minutes, second = divmod(diff_time.days * seconds_in_day + diff_time.seconds, 60)
        if minutes > TIMEOUT_FOR_OPEN_SESSION_MINUTES:
            print("To much time pass, CREATE NEW SESSION")
            session = None
        else:
            print("SESSION is still open!")

    if not session:
        print("Hi " + user_id + " You are new!:")
        # Initialize a ConversationSession object to track the call flow for this user
        session = ConversationSession(user_id)
        session.increment_call_flow()
    else:
        print("Hi " + user_id + " You are known!:")

    # Loop through the conversation flow
    while True:
        # call step
        current_conversation_step = str(session.get_call_flow_location())
        if current_conversation_step == "3":
            choices = ["ב", "א"]
            # Get user input
            user_input = input(f"{conversation_steps[current_conversation_step]}\n{choices}\n").lower()
        else:
            # Get user input
            user_input = input(f"{conversation_steps[current_conversation_step]}\n").lower()
        if not session.validate_user_input(user_input):
            continue
        # Add the user input to the ConversationSession object
        session.increment_call_flow()
        after_action_conversation_step = str(session.get_call_flow_location())
        # Check if conversation reach to last step
        if after_action_conversation_step == str(len(conversation_steps)):  # 7
            session.issue_to_be_created = user_input
            print(f"recevied message: '{session.issue_to_be_created}'")
            print(f"{conversation_steps[after_action_conversation_step]}\n")
            break


def chat_whatsapp(user_msg):
    # Get the user's name
    user_id = send_response_using_whatsapp_api(f"{conversation_steps['1']}\n")
    session = None
    conversation_history_ids = [item.get_user_id() for item in conversation_history]
    if user_id in conversation_history_ids:
        session = conversation_history[conversation_history_ids.index(user_id)]
        diff_time = datetime.now() - session.start_data
        seconds_in_day = 24 * 60 * 60
        minutes, second = divmod(diff_time.days * seconds_in_day + diff_time.seconds, 60)
        if minutes > TIMEOUT_FOR_OPEN_SESSION_MINUTES:
            print("To much time pass, CREATE NEW SESSION")
            send_response_using_whatsapp_api("To much time pass, CREATE NEW SESSION")
            session = None
        else:
            print("SESSION is still open!")
            # send_response_using_whatsapp_api("SESSION is still open!")

    if not session:
        print("Hi " + user_id + " You are new!:")
        # Print a greeting message and the predefined conversation steps
        print(conversation["Greeting"])
        send_response_using_whatsapp_api(conversation["Greeting"])
        for key, value in conversation_steps.items():
            print(f"{value} - {key}")
            # send_response_using_whatsapp_api(f"{value} - {key}")

        # Initialize a ConversationSession object to track the call flow for this user
        session = ConversationSession(user_id)
        session.increment_call_flow()
    else:
        print("Hi " + user_id + " You are known!:")

    # Loop through the conversation flow
    # while True:
    # call step
    current_conversation_step = str(session.get_call_flow_location())
    if current_conversation_step == "3":
        choices = ["ב", "א"]
        # Get user input
        user_input = send_response_using_whatsapp_api(
            f"{conversation_steps[current_conversation_step]}\n{choices}\n").lower()
    else:
        # Get user input
        user_input = send_response_using_whatsapp_api(f"{conversation_steps[current_conversation_step]}\n").lower()
    if not session.validate_user_input(user_input):
        return
    # Add the user input to the ConversationSession object
    session.increment_call_flow()
    after_action_conversation_step = str(session.get_call_flow_location())
    # Check if conversation reach to last step
    if after_action_conversation_step == str(len(conversation_steps)):  # 7
        session.issue_to_be_created = user_input
        print(f"recevied message: '{session.issue_to_be_created}'")
        send_response_using_whatsapp_api(f"recevied message: '{session.issue_to_be_created}'")
        print(f"{conversation_steps[after_action_conversation_step]}\n")
        send_response_using_whatsapp_api(f"{conversation_steps[after_action_conversation_step]}\n")
        return


def send_response_using_whatsapp_api(message):
    """Send a message using the WhatsApp Business API."""
    try:
        print(f"Sending response for: '{message}'")
        url = f"{FACEBOOK_API_URL}/{PHONE_NUMBER_ID_PROVIDER}/messages"

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
        print(f"Payload '{payload}'")
        print(f"Headers '{headers}'")
        response = requests.post(url, json=payload, headers=headers, verify=False)
        if not response.ok:
            return f"Failed to send message, json : '{payload}'  response: '{response}'"
        print(f"Message sent successfully to :'{to}'!")
        return f"Message sent successfully to :'{to}'!"
    except Exception as EX:
        return f"Error send response : '{EX}'"


def webhook():
    print(request)
    res = request.get_json()
    print(res)
    try:
        if res['entry'][0]['changes'][0]['value']['messages'][0]['id']:
            send_response_using_whatsapp_api("Thank you for the response.")
    except:
        print("Error on webhook()")
        pass
    return '200 OK HTTPS.'


def verify_token(req):
    if req.args.get("hub.mode") == "subscribe" and req.args.get("hub.challenge"):
        if not req.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token missmatch", 403
        return req.args['hub.challenge'], 200
    return "Hello world", 200


if __name__ == "__main__":
    app.run(debug=True, port=PORT)
    # app.run(host='0.0.0.0', port=5000)
