from datetime import datetime


class ConversationSession:
    conversation_steps = {
        "1": "אנא הזן שם משתמש",
        "2": "אנא הזן סיסמא",
        "3": "תודה שפנית אלינו, פרטיך נקלטו במערכת, באיזה נושא נוכל להעניק לך שירות?",
        "4": "בחר שירות",
        "5": "אנא הזן קוד מוצר",
        "6": "האם לחזור למספר הסלולרי?",
        "7": "נא רשום בקצרה את תיאור הפנייה",
        "8": "פנייתך התקבלה, נציג טלפוני יחזור אליך בהקדם.",
    }

    def __init__(self, user_id):
        self.user_id = user_id
        self.password = "11"
        self.call_flow_location = 1
        self.issue_to_be_created = None
        self.start_data = datetime.now()

    def increment_call_flow(self):
        self.call_flow_location += 1

    def get_conversation_session_id(self):
        return self.user_id

    def get_user_id(self):
        return self.user_id

    def get_call_flow_location(self):
        return self.call_flow_location

    def validate_user_input(self, user_input):
        if self.all_validation(user_input):
            return True
        return False

    def all_validation(self, step):
        # self.conversation_steps[self.call_flow_location]
        return True
