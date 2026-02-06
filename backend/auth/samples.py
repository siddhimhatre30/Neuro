import cv2
import os

# ================== CONFIG ==================
CASCADE_PATH = "backend/auth/haarcascade_frontalface_default.xml"
DATASET_PATH = "backend/auth/dataset"
IMAGE_COUNT = 30
MIN_FACE_SIZE = 100
# ============================================

# Load face detector
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

# Ask user name
name = input("Enter person name: ").strip()

if not name:
    print("❌ Name cannot be empty")
    exit()

# Create user folder
user_path = os.path.join(DATASET_PATH, name)
os.makedirs(user_path, exist_ok=True)

# Start camera
cam = cv2.VideoCapture(0)
if not cam.isOpened():
    print("❌ Camera not accessible")
    exit()

print("\n📸 Look at the camera. Capturing faces...")

count = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("❌ Failed to grab frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    for (x, y, w, h) in faces:
        if w < MIN_FACE_SIZE or h < MIN_FACE_SIZE:
            continue

        count += 1
        face_img = gray[y:y+h, x:x+w]
        img_path = os.path.join(user_path, f"{count}.jpg")
        cv2.imwrite(img_path, face_img)

        # Draw rectangle
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"{count}/{IMAGE_COUNT}",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    cv2.imshow("Face Samples", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC key
        break
    if count >= IMAGE_COUNT:
        break

# Cleanup
cam.release()
cv2.destroyAllWindows()

print(f"\n✅ {count} face samples saved for '{name}'")
