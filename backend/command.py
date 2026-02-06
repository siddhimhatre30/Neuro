import time
import eel
import pyttsx3
import speech_recognition as sr
from datetime import datetime
import webbrowser
import os
import shutil
from backend.voices import speak
from backend.intents import handle_intent


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



# ================== MAIN ==================
@eel.expose
def allCommands(message=1):

    query = takecommand() if message == 1 else message
    query = query.lower().strip()
    eel.senderText(query)

    try:
        intent_reply = handle_intent(query)
        if intent_reply:
            eel.ShowHood()
            return
        # ---------------- SEARCH ----------------
        if query.startswith("search"):
            search_google(query)

        # ---------------- CREATE FOLDER ----------------
        elif "create folder" in query or "make folder" in query:
            createFolderCommand(query)

        # ---------------- DELETE FOLDER ----------------
        elif "delete folder" in query or "remove folder" in query:
            deleteFolderCommand(query)

        # ---------------- OPEN APPS / FILES ----------------
        elif query.startswith("open"):
            from backend.features import openCommand
            openCommand(query)
        # ▶ PLAY SONG ON YOUTUBE
        elif "play" in query and "youtube" in query:
            from backend.features import playYouTube
            playYouTube(query)

        # ---------------- SEND WHATSAPP MESSAGE ----------------
        elif "send message" in query:
            from backend import features

            contact_no, name = features.findContact(query)
            if contact_no == 0:
                return

            speak("What message should I send?")
            msg = takecommand()
            features.whatsApp(contact_no, msg, "message", name)

        elif "whatsapp call" in query or "call on whatsapp" in query:
            from backend import features
            contact_no, name = features.findContact(query)
            if contact_no == 0:
                return
            features.whatsApp(contact_no, "", "call", name)
        elif "video call" in query or "whatsapp video" in query:
            from backend import features
            contact_no, name = features.findContact(query)
            if contact_no == 0:
                return
            features.whatsApp(contact_no, "", "video", name)
        elif "call" in query:
            from backend import features
            contact_no, name = features.findContact(query)
            if contact_no == 0:
                return
            features.normalPhoneCall(contact_no, name)


        # ---------------- CHATBOT FALLBACK ----------------
        else:
            from backend.chatbot import chatbot_response
            reply = chatbot_response(query)
            if reply:
                speak(reply)

    except Exception as e:
        print("Command Error:", e)

    eel.ShowHood()
