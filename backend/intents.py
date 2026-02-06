from datetime import datetime
from backend.voices import speak

INTENTS = {
    "greeting": {
        "keywords": ["hi", "hello", "hey"],
        "response": "Hello! How can I help you?"
    },

    "identity": {
        "keywords": ["your name", "who are you", "about yourself"],
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
                    reply = datetime.now().strftime("%I:%M %p")

                elif data["response"] == "DATE":
                    reply = datetime.now().strftime("%A, %d %B %Y")

                else:
                    reply = data["response"]

                speak(reply)

                if intent == "exit":
                    exit()

                return reply   # 🔥 IMPORTANT

    return None
