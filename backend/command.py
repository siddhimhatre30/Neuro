import time
import eel
import pyttsx3
import speech_recognition as sr
from datetime import datetime
import webbrowser
import os
import shutil


# ================== SPEAK ==================
def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    eel.receiverText(text)
    engine.say(text)
    engine.runAndWait()


# ================== TAKE COMMAND ==================
def takecommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        eel.DisplayMessage("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=10, phrase_time_limit=6)

    try:
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        eel.DisplayMessage(query)
        return query.lower()
    except:
        return ""


# ================== CREATE FOLDER ==================
def createFolderCommand(query):
    query = query.lower()
    for w in ["create", "make", "folder"]:
        query = query.replace(w, "")
    query = query.strip()

    base_path = os.path.join(os.path.expanduser("~"), "Desktop")

    if "c drive" in query:
        base_path = "C:\\"
        query = query.replace("c drive", "")
    elif "d drive" in query:
        base_path = "D:\\"
        query = query.replace("d drive", "")
    elif "desktop" in query:
        query = query.replace("desktop", "")

    folder_name = query.strip()
    if not folder_name:
        speak("Please tell the folder name")
        return

    path = os.path.join(base_path, folder_name)

    try:
        os.makedirs(path, exist_ok=True)
        speak(f"Folder {folder_name} created")
    except:
        speak("Unable to create folder")


# ================== DELETE FOLDER (NO CONFIRMATION) ==================
def deleteFolderCommand(query):
    query = query.lower()
    for w in ["delete", "remove", "folder"]:
        query = query.replace(w, "")
    query = query.strip()

    base_path = os.path.join(os.path.expanduser("~"), "Desktop")

    if "c drive" in query:
        base_path = "C:\\"
        query = query.replace("c drive", "")
    elif "d drive" in query:
        base_path = "D:\\"
        query = query.replace("d drive", "")
    elif "desktop" in query:
        query = query.replace("desktop", "")

    folder_name = query.strip()
    if not folder_name:
        speak("Please tell the folder name")
        return

    folder_path = os.path.join(base_path, folder_name)

    if not os.path.exists(folder_path):
        speak("Folder not found")
        return

    try:
        shutil.rmtree(folder_path)
        speak(f"Folder {folder_name} deleted")
    except Exception as e:
        print("Delete error:", e)
        speak("Unable to delete folder")


# ================== GOOGLE SEARCH ==================
def search_google(query):
    speak("Searching on Google")
    query = query.replace("search", "").strip()
    url = "https://www.google.com/search?q=" + query.replace(" ", "+")
    webbrowser.open(url)


# ================== INTENTS ==================
INTENTS = {
    "greeting": {"keywords": ["hi", "hello"], "response": "Hello"},
    "time": {"keywords": ["time"], "response": "TIME"},
    "date": {"keywords": ["date"], "response": "DATE"},
    "exit": {"keywords": ["exit", "bye"], "response": "Goodbye"}
}


def handle_intent(query):
    for intent, data in INTENTS.items():
        for k in data["keywords"]:
            if k in query:
                if data["response"] == "TIME":
                    speak(datetime.now().strftime("%I:%M %p"))
                elif data["response"] == "DATE":
                    speak(datetime.now().strftime("%A, %d %B %Y"))
                else:
                    speak(data["response"])
                if intent == "exit":
                    exit()
                return True
    return False
def ask_open_image(image_name, location=None):
    search_paths = [
        os.path.join(os.path.expanduser("~"), "Desktop"),
        os.path.join(os.path.expanduser("~"), "Downloads"),
        "C:\\",
        "D:\\"
    ]

    for base in search_paths:
        for root, dirs, files in os.walk(base):
            for file in files:
                name, ext = os.path.splitext(file)
                if name.lower() == image_name.lower() and ext.lower() in [".jpg", ".png", ".jpeg"]:
                    os.startfile(os.path.join(root, file))
                    speak(f"Opening image {image_name}")
                    return

    speak("Image not found")


# ================== MAIN ==================
@eel.expose
def allCommands(message=1):

    query = takecommand() if message == 1 else message
    eel.senderText(query)

    try:
        if query.startswith("search"):
            search_google(query)

        elif "create folder" in query or "make folder" in query:
            createFolderCommand(query)

        elif "delete folder" in query or "remove folder" in query:
            deleteFolderCommand(query)

        elif "open" in query:
            from backend.features import openCommand
            openCommand(query)
        elif "send message" in query or "phone call" in query or "video call" in query: 
            from backend.features import findContact, whatsApp 

            contact_no, name = findContact(query)

            if contact_no == 0:
                return   # 🚑 STOP if contact not found

            if "send message" in query:
                speak("What message should I send?")
                msg = takecommand()
                whatsApp(contact_no, msg, "message", name)

            elif "phone call" in query:
                whatsApp(contact_no, "", "call", name)

            elif "video call" in query:
                whatsApp(contact_no, "", "video", name)

        elif handle_intent(query):
            return

        else:
            from backend.chatbot import chatbot_response
            reply = chatbot_response(query)
            if reply:
                speak(reply)

    except Exception as e:
        print("Error:", e)

    eel.ShowHood()
