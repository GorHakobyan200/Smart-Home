import face_recognition
import cv2
import numpy as np
from twilio.rest import Client
import sys
import pyttsx3


def talk(words):
    engine = pyttsx3.init()
    engine.say(words)
    engine.runAndWait()

                
                
                
account_sid = ""

auth_token  = "dfcAC81e1ee14372cb96e803c98a6017eefc443e5f925d0cf6223cd1b07c5c60f5"
client = Client(account_sid, auth_token)



video_capture = cv2.VideoCapture(0)

gor_image = face_recognition.load_image_file("gor.jpg")
gor_face_encoding = face_recognition.face_encodings(gor_image)[0]



known_face_encodings = [
    gor_face_encoding
]
known_face_names = [
    "Gor Hakobyan"
]

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    ret, frame = video_capture.read()

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = []

        for face_location in face_locations:
            try:
                encodings = face_recognition.face_encodings(rgb_small_frame, [face_location])
                if encodings:  # Check if encoding was successful
                    face_encodings.append(encodings[0])
            except Exception as e:
                print(f"Encoding failed for a face: {e}")

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if name == "Unknown":
                message = client.messages.create(
                    to="+37443880078", 
                    from_="+19896144599",
                    body="Չհայնաբերված անձ"
                )
                return_value,image = video_capture.read()
                cv2.imwrite('Unknown Person.png', image)
                talk("Unknown Person found,please go away")


            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

            if name == "Gor Hakobyan":
               talk("Face Recognized")
               sys.exit("Face Recognized")



    process_this_frame = not process_this_frame


    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
