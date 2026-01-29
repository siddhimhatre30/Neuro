from datetime import datetime
import pyttsx3

# text-to-speech (since you already use pyttsx3)
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()


INTENTS = {
    "greeting": {
        "keywords": ["hi", "hello", "hey"],
        "response": "Hello! How can I help you?"
    },

    "identity": {
        "keywords": ["your name", "who are you","tell me about yourself"],
        "response": "I am Neuro, your AI assistant."
    },

    "time": {
        "keywords": ["time", "clock"],
        "response": "TIME"
    },

    "date": {
        "keywords": ["date", "day"],
        "response": "DATE"
    },

    "exit": {
        "keywords": ["bye", "exit", "quit"],
        "response": "Goodbye! Have a great day."
    }
}


def handle_intent(query):
    query = query.lower()

    for intent, data in INTENTS.items():
        for keyword in data["keywords"]:
            if keyword in query:

                if data["response"] == "TIME":
                    now = datetime.now().strftime("%I:%M %p")
                    speak(f"The time is {now}")
                    return True

                if data["response"] == "DATE":
                    today = datetime.now().strftime("%A, %d %B %Y")
                    speak(f"Today is {today}")
                    return True

                speak(data["response"])

                if intent == "exit":
                    exit()

                return True

    return False
