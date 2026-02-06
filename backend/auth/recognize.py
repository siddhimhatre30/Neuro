import cv2
import json
import os

CASCADE_PATH = "backend/auth/haarcascade_frontalface_default.xml"
TRAINER_PATH = "backend/auth/trainer/trainer.yml"
LABELS_PATH = "backend/auth/trainer/labels.json"
CONFIDENCE_THRESHOLD = 50


def AuthenticateFace():
    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(TRAINER_PATH)

    with open(LABELS_PATH, "r") as f:
        label_map = json.load(f)

    label_map = {int(k): v for k, v in label_map.items()}

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("❌ Camera not accessible")
        return False

    print("\n🎥 Face recognition started (ESC to exit)")

    authenticated = False

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_img = gray[y:y+h, x:x+w]
            face_id, confidence = recognizer.predict(face_img)

            if face_id in label_map and confidence <= CONFIDENCE_THRESHOLD:
                name = label_map[face_id]
                authenticated = True
                print(f"✅ Authenticated: {name}")
                cam.release()
                cv2.destroyAllWindows()
                return True

        cv2.imshow("Face Authentication", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cam.release()
    cv2.destroyAllWindows()
    return False
