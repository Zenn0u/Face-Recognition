import face_recognition
import cv2
import os

from face_recognition.api import face_locations

KNOWN_DIR = "known"
UNKNOWN_DIR = "unknown"

TOLERANCE = 0.6
FRAME_THICKNESS = 3
FONT_THICKNESS = 1
MODEL = "cnn"

# Loading Faces

known_faces = []
known_names = []

for name in os.listdir(KNOWN_DIR):
    for filename in os.listdir(f"{KNOWN_DIR}/{name}"):
        image = face_recognition.load_image_file(f"{KNOWN_DIR}/{name}/{filename}")
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_names.append(name)

for filename in os.listdir(UNKNOWN_DIR):
    image = face_recognition.load_image_file(f"{UNKNOWN_DIR}/{filename}")
    image = cv2.resize(image, (1280, 800))
    locations = face_recognition.face_locations(image, model=MODEL)
    encodings = face_recognition.face_encodings(image, locations)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    for face_encoding, face_location in zip(encodings, locations):
        results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)
        match = None
        if True in results:
            match = known_names[results.index(True)]
            print(f"Match Found: {match}")

            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2])

            color = [0, 0, 255]

            cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)

            top_left = (face_location[3], face_location[2])
            bottom_right = (face_location[1], face_location[2]+20)
            cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
            cv2.putText(image, match, (face_location[3]+10, face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), FONT_THICKNESS)

    cv2.imshow(filename, image)
    cv2.waitKey(0)
    cv2.destroyWindow(filename)       