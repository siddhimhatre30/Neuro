import time

last_active_time = time.time()

def check_timeout(timeout=30):
    global last_active_time
    if time.time() - last_active_time > timeout:
        print("⏱ Session refreshed")
    last_active_time = time.time()
