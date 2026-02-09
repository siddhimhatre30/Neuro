import cv2
import json
import time

# ================= CONFIG =================
CASCADE_PATH = "backend/auth/haarcascade_frontalface_default.xml"
TRAINER_PATH = "backend/auth/trainer/trainer.yml"
LABELS_PATH = "backend/auth/trainer/labels.json"

CONFIDENCE_THRESHOLD = 65      # LBPH: lower = better
REQUIRED_GOOD_FRAMES = 3
AUTH_TIMEOUT = 15              # seconds
MIN_FACE_SIZE = 120
# =========================================


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

    print("\n🎥 Face authentication started (ESC to cancel)")

    success_frames = 0
    start_time = time.time()
    face_seen = False

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=6,
            minSize=(MIN_FACE_SIZE, MIN_FACE_SIZE)
        )

        for (x, y, w, h) in faces:
            face_seen = True
            face_img = gray[y:y+h, x:x+w]
            face_id, confidence = recognizer.predict(face_img)

            if face_id in label_map and confidence <= CONFIDENCE_THRESHOLD:
                success_frames += 1
                name = label_map[face_id]
                color = (0, 255, 0)
                text = f"{name} ({int(confidence)})"
            else:
                success_frames = 0
                color = (0, 0, 255)
                text = "Unknown"

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(
                frame, text,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8, color, 2
            )

            if success_frames >= REQUIRED_GOOD_FRAMES:
                print(f"✅ Authenticated: {name}")
                cam.release()
                cv2.destroyAllWindows()
                return True

        cv2.imshow("Face Authentication", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

        if time.time() - start_time > AUTH_TIMEOUT:
            break

    cam.release()
    cv2.destroyAllWindows()

    if not face_seen:
        print("❌ No face detected")
    else:
        print("❌ Face authentication failed")

    return False
