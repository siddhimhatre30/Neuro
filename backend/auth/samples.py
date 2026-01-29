import cv2
import os

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(3, 640)
cam.set(4, 480)

detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

face_id = input("Enter a Numeric user ID here: ")

# Create samples directory if not exists
if not os.path.exists("backend/auth/samples"):
    os.makedirs("backend/auth/samples")

print("Taking samples, look at camera .......")
count = 0

while True:
    ret, img = cam.read()
    if not ret:
        print("Camera not detected")
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        count += 1

        cv2.imwrite(
            f"backend/auth/samples/face.{face_id}.{count}.jpg",
            gray[y:y + h, x:x + w]
        )

        cv2.imshow("image", img)

    if cv2.waitKey(100) & 0xff == 27 or count >= 100:
        break

print("Samples taken, closing program...")
cam.release()
cv2.destroyAllWindows()


