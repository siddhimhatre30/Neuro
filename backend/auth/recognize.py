import cv2
import time


def AuthenticateFace():

    # ---------- CONFIG ----------
    THRESHOLD = 65            # based on your distances
    REQUIRED_MATCHES = 3      # consecutive frames required
    MAX_RUNTIME = 10          # seconds
    # ----------------------------

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('backend\\auth\\trainer\\trainer.yml')

    cascadePath = "backend\\auth\\haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)

    names = ['', 'Siddhi', 'Harchit']

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)
    cam.set(4, 480)

    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    font = cv2.FONT_HERSHEY_SIMPLEX

    match_count = 0
    flag = 0
    start_time = time.time()

    while True:

        # timeout safety
        if time.time() - start_time > MAX_RUNTIME:
            break

        ret, img = cam.read()
        if not ret:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )

        detected_this_frame = False

        for (x, y, w, h) in faces:

            # ignore tiny / noisy boxes
            if w < 80 or h < 80:
                continue

            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

            face_img = gray[y:y+h, x:x+w]
            face_id, distance = recognizer.predict(face_img)

            print("Predicted ID:", face_id, "Distance:", distance)

            if distance <= THRESHOLD and face_id in [1, 2]:
                match_count += 1
                name = names[face_id]
                confidence = f"{round(100 - distance)}%"
                detected_this_frame = True
            else:
                match_count = 0
                name = "Unknown"
                confidence = "0%"

            cv2.putText(img, name, (x+5, y-5),
                        font, 1, (255, 255, 255), 2)
            cv2.putText(img, confidence, (x+5, y+h-5),
                        font, 1, (255, 255, 0), 1)

            # accept only after multiple confirmations
            if match_count >= REQUIRED_MATCHES:
                flag = 1
                break

        if not detected_this_frame:
            match_count = 0

        cv2.imshow('camera', img)

        if cv2.waitKey(10) & 0xff == 27 or flag == 1:
            break

    cam.release()
    cv2.destroyAllWindows()
    return flag
