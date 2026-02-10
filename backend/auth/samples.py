import cv2
import os
import time

# ================= CONFIG =================
CASCADE_PATH = "backend/auth/haarcascade_frontalface_default.xml"
DATASET_PATH = "backend/auth/dataset"
TOTAL_SAMPLES = 40
MIN_FACE_SIZE = 120
CAPTURE_DELAY = 0.3   # seconds between captures
# =========================================


# ---------- Safety checks ----------
if not os.path.exists(CASCADE_PATH):
    print("❌ Haarcascade file not found")
    exit()

face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

# ---------- Get person name ----------
person_name = input("Enter person name: ").strip()

if not person_name.isalpha():
    print("❌ Invalid name. Use only letters (A–Z)")
    exit()

# ---------- Create folder ----------
person_path = os.path.join(DATASET_PATH, person_name)
os.makedirs(person_path, exist_ok=True)

# ---------- Camera ----------
cam = cv2.VideoCapture(0)
if not cam.isOpened():
    print("❌ Camera not accessible")
    exit()

print("\n📸 Collecting face samples")
print("➡️ Ensure ONLY this person is in front of camera")
print("➡️ Move head slightly (left / right / up / smile)")
print("➡️ Press ESC to stop\n")

count = 0
last_capture = time.time()

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

    # Allow only ONE face
    if len(faces) == 1:
        (x, y, w, h) = faces[0]

        if time.time() - last_capture >= CAPTURE_DELAY:
            face_img = gray[y:y+h, x:x+w]
            count += 1

            img_path = os.path.join(person_path, f"{count}.jpg")
            cv2.imwrite(img_path, face_img)
            last_capture = time.time()

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    elif len(faces) > 1:
        cv2.putText(
            frame,
            "Multiple faces detected!",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 0, 255),
            2
        )

    cv2.putText(
        frame,
        f"Samples: {count}/{TOTAL_SAMPLES}",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.imshow("Face Sample Collection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        print("⏹ Stopped by user")
        break

    if count >= TOTAL_SAMPLES:
        break

# ---------- Cleanup ----------
cam.release()
cv2.destroyAllWindows()

print(f"\n✅ {count} samples saved for '{person_name}'")
print(f"📂 Location: {person_path}")
