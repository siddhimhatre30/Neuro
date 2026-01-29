import eel
import os
from backend.features import *
from backend.command import *
from backend.auth import recognize
def start():
    playAssistantSound()
    eel.init('frontend')
    @eel.expose
    def init():
        eel.hideLoader()
        speak("Ready for face authentication")
        flag=recognize.AuthenticateFace()
        if flag==1:
            eel.hideFaceAuth()
            speak("Face Authentication successfully")
            eel.hideFaceAuthSuccess()
            eel.hideStart()
            playAssistantSound()
        else:
            speak("Face Authentication failed")

    os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    eel.start('index.html', mode=None, host='localhost', block=True)
    
