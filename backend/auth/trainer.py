import cv2
import numpy as np
from PIL import Image
import os

# ================== PATHS ==================
SAMPLES_PATH = "backend/auth/samples"
TRAINER_PATH = "backend/auth/trainer"

# Create trainer directory if it doesn't exist
if not os.path.exists(TRAINER_PATH):
    os.makedirs(TRAINER_PATH)

# ================== FACE RECOGNIZER ==================
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Use OpenCV built-in haarcascade path (SAFE)
detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


# ================== FUNCTION TO GET IMAGES & LABELS ==================
def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    ids = []

    for imagePath in imagePaths:

        # Convert image to grayscale
        gray_img = Image.open(imagePath).convert('L')
        img_arr = np.array(gray_img, 'uint8')

        # Get ID from image filename: face.id.count.jpg
        try:
            id = int(os.path.split(imagePath)[-1].split(".")[1])
        except:
            continue

        faces = detector.detectMultiScale(img_arr)

        for (x, y, w, h) in faces:
            faceSamples.append(img_arr[y:y + h, x:x + w])
            ids.append(id)

    return faceSamples, ids


# ================== TRAINING ==================
print("Training faces. This may take a few seconds...")

faces, ids = getImagesAndLabels(SAMPLES_PATH)

if len(faces) == 0:
    print("No faces found! Please collect face samples first.")
    exit()

recognizer.train(faces, np.array(ids))

# Save trained model
recognizer.write(os.path.join(TRAINER_PATH, "trainer.yml"))

print("Model trained successfully!")
print("Saved as backend/auth/trainer/trainer.yml")
print("Now you can recognize faces")
