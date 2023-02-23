from datetime import datetime
from pprint import pprint


class ConversationSession:
    conversation_steps = {
        "1": "אנא הזן שם משתמש",
        "2": "אנא הזן סיסמא",
        "3": "תודה שפנית אלינו, פרטיך נקלטו במערכת, באיזה נושא נוכל להעניק לך שירות?",
        "4": "אנא הזן קוד מוצר",
        "5": "האם לחזור למספר הסלולרי?",
        "6": "נא רשום בקצרה את תיאור הפנייה",
        "7": "פנייתך התקבלה, נציג טלפוני יחזור אליך בהקדם.",
    }
    conversation_steps_response = {"1": "",
                                   "2": "",
                                   "3": "",
                                   "4": "",
                                   "5": "",
                                   "6": ""
                                   }

    def __init__(self, user_id):
        self.user_id = user_id
        self.password = "11"
        self.call_flow_location = 1
        self.issue_to_be_created = None
        self.start_data = datetime.now()
        self.session_active = True

    def increment_call_flow(self):
        self.call_flow_location += 1
        print(f"call flow inc to: '{self.call_flow_location}'")

    def get_conversation_session_id(self):
        return self.user_id

    def get_user_id(self):
        return self.user_id

    def get_call_flow_location(self):
        return self.call_flow_location

    def validate_user_input(self, user_input):
        if self.all_validation(self.call_flow_location, user_input):
            return True
        return False

    # def all_validation(self, step, answer):
    #     match step:
    #         case 1:
    #             print(f"Check if user name '{answer}' valid")
    #         case 2:
    #             print(f"Check if password '{answer}' valid")
    #             print(
    #                 f"Search for user with user name '{self.conversation_steps_response['1']}' and password '{answer}'")
    #         case 3:
    #             print(f"check if chosen '{answer}' valid")
    #             if answer not in ['ב', 'א']:
    #                 return False
    #         case 4:
    #             print(f"Check if product '{answer}' exist")
    #         case 5:
    #             print(f"Check if phone number '{answer}' is valid")
    #         case 6:
    #             print(f"NO NEED TO VALIDATE ISSUE")
    #     return True

    def validation_switch_step(self, case, answer):
        if case == 1:
            print(f"Check if user name '{answer}' valid")
        elif case == 2:
            print(f"Check if password '{answer}' valid")
            print(
                f"Search for user with user name '{self.conversation_steps_response['1']}' and password '{answer}'")
        elif case == 3:
            print(f"check if chosen '{answer}' valid")
            if answer not in ['ב', 'א']:
                return False
        elif case == 4:
            print(f"Check if product '{answer}' exist")
        elif case == 5:
            print(f"Check if phone number '{answer}' is valid")
        elif case == 6:
            print(f"NO NEED TO VALIDATE ISSUE")
        else:
            return False
        return True

    def validate_and_set_answer(self, step, response):
        step = int(step) - 1
        # if self.all_validation(step, response):
        if self.validation_switch_step(step, response):
            print(f"{self.conversation_steps[str(step)]}: {response}")
            self.conversation_steps_response[str(step)] = response
            result = f"{self.conversation_steps[str(step)]}: {response}"
            return True, result
        else:
            print(f"Not valid response {response}")
            result = f" ערך לא חוקי '{response}' "
            return False, result

    def set_status(self, status):
        self.session_active = status

    def get_chossies(self, step):
        choices = ["ב", "א"]

    def print_all_flow_call(self):
        pprint(self.conversation_steps_response)
