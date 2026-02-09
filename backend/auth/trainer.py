import cv2
import os
import json
import numpy as np
from PIL import Image

# ================= CONFIG =================
DATASET_PATH = "backend/auth/dataset"
TRAINER_DIR = "backend/auth/trainer"
TRAINER_PATH = os.path.join(TRAINER_DIR, "trainer.yml")
LABELS_PATH = os.path.join(TRAINER_DIR, "labels.json")
# =========================================

os.makedirs(TRAINER_DIR, exist_ok=True)

recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
labels = []
label_map = {}

current_id = 1

print("\n📂 Loading dataset...")

for person_name in sorted(os.listdir(DATASET_PATH)):
    person_path = os.path.join(DATASET_PATH, person_name)

    if not os.path.isdir(person_path):
        continue

    print(f"➡️ {person_name} → ID {current_id}")
    label_map[current_id] = person_name

    for img_name in os.listdir(person_path):
        if not img_name.lower().endswith((".jpg", ".png", ".jpeg")):
            continue

        img_path = os.path.join(person_path, img_name)
        img = Image.open(img_path).convert("L")
        img_np = np.array(img, "uint8")

        faces.append(img_np)
        labels.append(current_id)

    current_id += 1

if len(faces) == 0:
    print("❌ No training images found")
    exit()

print("\n🧠 Training face recognizer...")
recognizer.train(faces, np.array(labels))

recognizer.save(TRAINER_PATH)

with open(LABELS_PATH, "w") as f:
    json.dump(label_map, f, indent=4)

print("\n✅ Training complete")
print(f"📁 trainer.yml saved at: {TRAINER_PATH}")
print(f"🗂 labels.json saved at: {LABELS_PATH}")
