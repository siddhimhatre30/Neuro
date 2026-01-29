import struct
import time
import pvporcupine
import pyaudio
import pyautogui

def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        porcupine = pvporcupine.create(
            access_key="+F6Kx3uBBTLYfz/CGPjJ337x5Ug9C+IInFTq+OwUhL3YvBpqH302Hw==",  # 👈 Add your key here
            keyword_paths=[r"jjC:\Users\LENOVO\Downloads\Hey-neuro_en_windows_v4_0_0 (1)\Hey-neuro_en_windows_v4_0_0.ppn"]
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

hotword()
