import json
import os
import re
from shlex import quote
import sqlite3
import struct
import subprocess
import time
import webbrowser
from playsound import playsound
import eel
import pvporcupine
import pyaudio
import pyautogui
from backend.voices import speak
from backend.config import ASSISTANT_NAME
import pywhatkit as kit
from backend.helper import extract_yt_term, remove_words
import pygetwindow as gw
conn = sqlite3.connect('neuro.db')
cursor = conn.cursor()

@eel.expose
def playAssistantSound():
    music_dir="frontend\\assets\\audio\\frontend_assets_audio_start_sound.mp3"
    playsound(music_dir)


def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.replace("folder", "")
    query = query.replace("the", "")
    query = query.lower().strip()

    if query == "":
        return

    try:
        # 1️⃣ SYSTEM COMMAND (apps, drives)
        cursor.execute(
            "SELECT path FROM sys_command WHERE name = ?", (query,))
        results = cursor.fetchall()

        if len(results) != 0:
            speak("Opening " + query)
            os.startfile(results[0][0])
            return

        # 2️⃣ FILE / FOLDER COMMAND (pdf, folders like games)
        cursor.execute(
            "SELECT path FROM file_command WHERE name = ?", (query,))
        file_result = cursor.fetchall()

        if len(file_result) != 0:
            speak("Opening " + query)
            os.startfile(file_result[0][0])
            return

        # 3️⃣ WEB COMMAND
        cursor.execute(
            "SELECT url FROM web_command WHERE name = ?", (query,))
        web_result = cursor.fetchall()

        if len(web_result) != 0:
            speak("Opening " + query)
            webbrowser.open(web_result[0][0])
            return

        # 4️⃣ FALLBACK
        speak("Opening " + query)
        os.system(f'start "" "{query}"')

    except Exception as e:
        print("ERROR:", e)
        speak("something went wrong")


def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)


def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        porcupine = pvporcupine.create(
            access_key="+F6Kx3uBBTLYfz/CGPjJ337x5Ug9C+IInFTq+OwUhL3YvBpqH302Hw==",  # 👈 Add your key here
            keyword_paths=[r"C:\Users\LENOVO\Downloads\Hey-neuro_en_windows_v4_0_0 (1)\Hey-neuro_en_windows_v4_0_0.ppn"]
        )

        paud = pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        print("🎧 Listening for 'Neuro'...")

        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)
            keyword_index = porcupine.process(keyword)

            if keyword_index >= 0:
                print("✅ Hotword 'Neuro' detected!")
                pyautogui.keyDown("win")
                pyautogui.press("j")
                time.sleep(2)
                pyautogui.keyUp("win")

    except KeyboardInterrupt:
        print("🛑 Stopped manually.")
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()
# find contacts
def playYouTube(query):
    song = query.replace("play", "").replace("on youtube", "").replace("youtube", "").strip()
    speak(f"Playing {song} on YouTube")
    kit.playonyt(song)

def findContact(query):
    words_to_remove = [
        ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call',
        'send', 'message', 'whatsapp', 'video'
    ]

    query = remove_words(query, words_to_remove)
    query = query.strip().lower()

    try:
        cursor.execute(
            "SELECT name, mobile_no FROM contacts WHERE LOWER(name) LIKE ?",
            ('%' + query + '%',)
        )
        result = cursor.fetchone()

        if not result:
            speak('Contact not found')
            return 0, 0

        name = result[0]
        mobile_no = str(result[1])

        # 🔥 CLEAN MOBILE NUMBER
        mobile_no = re.sub(r'\D', '', mobile_no)  # remove space, +, -

        if len(mobile_no) == 10:
            mobile_no = '91' + mobile_no

        mobile_no = '+' + mobile_no

        print("Calling number:", mobile_no)

        return mobile_no, name

    except Exception as e:
        print("findContact error:", e)
        speak('Contact not exist')
        return 0, 0
def open_whatsapp_desktop():
    try:
        subprocess.Popen("start whatsapp:", shell=True)
        time.sleep(8)  # give time to load
    except Exception as e:
        print("WhatsApp open error:", e)
        speak("WhatsApp desktop not found")
def wait_for_whatsapp():
    for _ in range(20):
        windows = gw.getWindowsWithTitle("WhatsApp")
        if windows:
            windows[0].activate()
            return True
        time.sleep(0.5)
    return False


def whatsApp(mobile_no, message, flag, name):

    if flag == "message":
        speak(f"Sending message to {name}")

        # open WhatsApp chat
        url = f"whatsapp://send?phone={mobile_no}&text={quote(message)}"
        subprocess.Popen(f'start "" "{url}"', shell=True)

        time.sleep(10)  # WhatsApp Desktop load time

        # 🔥 CLICK MESSAGE INPUT BOX (VERY IMPORTANT)
        pyautogui.click(1872,980)   # 👈 CHANGE THIS FOR YOUR SCREEN
        time.sleep(0.3)

        pyautogui.press("enter")
        speak("Message sent successfully")


    elif flag == "call":
        whatsapp_call_pyautogui(name, "voice")

    elif flag == "video":
        whatsapp_call_pyautogui(name, "video")
def whatsapp_call_pyautogui(name, call_type="voice"):
    open_whatsapp_desktop()

    # 1️⃣ Click search bar
    pyautogui.click(210,154)  # 🔴 CHANGE
    time.sleep(0.5)

    # 2️⃣ Type contact name
    pyautogui.write(name, interval=0.1)
    time.sleep(1)

    # 3️⃣ Open chat
    pyautogui.press("enter")
    time.sleep(2)
    # 1️⃣ Click call dropdown
    pyautogui.click(1694,87)
    time.sleep(0.8)
    # 4️⃣ Click call button
    if call_type == "voice":
        pyautogui.click(1453,240)  # 🔴 VOICE ICON
        speak(f"Calling {name}")

    elif call_type == "video":
        pyautogui.click(1662,243)  # 🔴 VIDEO ICON
        speak(f"Starting video call with {name}")


def normalPhoneCall(mobile_no, name):
    speak(f"Calling {name}. Please confirm the call on your phone or dialer.")
    subprocess.run(f'start tel:{mobile_no}', shell=True)



# Assistant name
@eel.expose
def assistantName():
    name = ASSISTANT_NAME
    return name

@eel.expose
def personalInfo():
    try:
        cursor.execute("SELECT * FROM info")
        results = cursor.fetchall()
        jsonArr = json.dumps(results[0])
        eel.getData(jsonArr)
        return 1    
    except:
        print("no data")

@eel.expose
def updatePersonalInfo(name, designation, mobileno, email, city):
    cursor.execute("SELECT COUNT(*) FROM info")
    count = cursor.fetchone()[0]

    if count > 0:
        # Update existing record
        cursor.execute(
            '''UPDATE info 
               SET name=?, designation=?, mobileno=?, email=?, city=?''',
            (name, designation, mobileno, email, city)
        )
    else:
        # Insert new record if no data exists
        cursor.execute(
            '''INSERT INTO info (name, designation, mobileno, email, city) 
               VALUES (?, ?, ?, ?, ?)''',
            (name, designation, mobileno, email, city)
        )

    conn.commit()
    personalInfo()
    return 1
@eel.expose
def displaySysCommand():
    cursor.execute("SELECT * FROM sys_command")
    results = cursor.fetchall()
    jsonArr = json.dumps(results)
    eel.displaySysCommand(jsonArr)
    return 1


@eel.expose
def deleteSysCommand(id):
    cursor.execute("DELETE FROM sys_command WHERE id = ?", (id,))
    conn.commit()


@eel.expose
def addSysCommand(key, value):
    cursor.execute(
        '''INSERT INTO sys_command VALUES (?, ?, ?)''', (None,key, value))
    conn.commit()


@eel.expose
def displayWebCommand():
    cursor.execute("SELECT * FROM web_command")
    results = cursor.fetchall()
    jsonArr = json.dumps(results)
    eel.displayWebCommand(jsonArr)
    return 1


@eel.expose
def addWebCommand(key, value):
    cursor.execute(
        '''INSERT INTO web_command VALUES (?, ?, ?)''', (None, key, value))
    conn.commit()


@eel.expose
def deleteWebCommand(id):
    cursor.execute("DELETE FROM web_command WHERE Id = ?", (id,))
    conn.commit()


@eel.expose
def displayPhoneBookCommand():
    cursor.execute("SELECT * FROM contacts")
    results = cursor.fetchall()
    jsonArr = json.dumps(results)
    eel.displayPhoneBookCommand(jsonArr)
    return 1


@eel.expose
def deletePhoneBookCommand(id):
    cursor.execute("DELETE FROM contacts WHERE Id = ?", (id,))
    conn.commit()


@eel.expose
def InsertContacts(Name, MobileNo, Email, City):
    cursor.execute(
        '''INSERT INTO contacts VALUES (?, ?, ?, ?, ?)''', (None,Name, MobileNo, Email, City))
    conn.commit()


def createFolderCommand(query):
    query = query.lower()
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("create", "")
    query = query.replace("make", "")
    query = query.replace("folder", "")
    query = query.strip()

    # default location → Desktop
    base_path = os.path.join(os.path.expanduser("~"), "Desktop")

    # detect drive
    if "c drive" in query:
        base_path = "C:\\"
        query = query.replace("c drive", "").strip()
    elif "d drive" in query:
        base_path = "D:\\"
        query = query.replace("d drive", "").strip()
    elif "e drive" in query:
        base_path = "E:\\"
        query = query.replace("e drive", "").strip()
    elif "desktop" in query:
        base_path = os.path.join(os.path.expanduser("~"), "Desktop")
        query = query.replace("desktop", "").strip()

    folder_name = query.strip()

    if folder_name == "":
        speak("Please tell folder name")
        return

    folder_path = os.path.join(base_path, folder_name)

    try:
        os.makedirs(folder_path, exist_ok=True)
        speak(f"Folder {folder_name} created")
    except Exception as e:
        print("ERROR:", e)
        speak("Unable to create folder")
