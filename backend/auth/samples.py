import cv2
import os

# ================= CONFIG =================
CASCADE_PATH = "backend/auth/haarcascade_frontalface_default.xml"
DATASET_PATH = "backend/auth/dataset"
TOTAL_SAMPLES = 40          # number of images to capture
MIN_FACE_SIZE = 120         # ignore very small faces
# =========================================

# Load Haar cascade
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

# Ask for person name
person_name = input("Enter person name: ").strip()

if person_name == "":
    print("❌ Name cannot be empty")
    exit()

# Create dataset folder for person
person_path = os.path.join(DATASET_PATH, person_name)
os.makedirs(person_path, exist_ok=True)

# Open camera
cam = cv2.VideoCapture(0)
if not cam.isOpened():
    print("❌ Camera not accessible")
    exit()

print("\n📸 Collecting face samples...")
print("➡️ Look straight, left, right, smile slightly")
print("➡️ Press ESC to stop early\n")

count = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("❌ Failed to read frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=6,
        minSize=(MIN_FACE_SIZE, MIN_FACE_SIZE)
    )

    for (x, y, w, h) in faces:
        face_img = gray[y:y+h, x:x+w]

        count += 1
        img_path = os.path.join(person_path, f"{count}.jpg")
        cv2.imwrite(img_path, face_img)

        # Draw rectangle and counter
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"{count}/{TOTAL_SAMPLES}",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    cv2.imshow("Face Sample Collection", frame)

    if cv2.waitKey(1) & 0xFF == 27:   # ESC key
        print("⏹ Sample collection stopped by user")
        break

    if count >= TOTAL_SAMPLES:
        break

# Cleanup
cam.release()
cv2.destroyAllWindows()

print(f"\n✅ {count} samples saved for '{person_name}'")
print(f"📂 Location: {person_path}")
