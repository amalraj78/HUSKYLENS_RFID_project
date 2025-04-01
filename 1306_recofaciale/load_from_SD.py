import time
import json
from huskylib import HuskyLensLibrary, Block

# Program Parameters
text_on = True
sms_interval = 10
last_sms_time = 0

# Change for your Serial Port
hl = HuskyLensLibrary("SERIAL", "/dev/ttyUSB0", 3000000)

def load_known_faces_from_sd(max_face_id):
    known_faces = {}
    for face_id in range(1, max_face_id + 1):
        print(f"loadmodelSD")
        response = hl.loadModelFromSDCard(face_id)
        print(f"Load model response for face ID {face_id}: {response}")
        if response and isinstance(response, list):
            for item in response:
                if isinstance(item, Block):
                    print(f"Adding face ID {item.ID} to known faces")
                    known_faces[item.ID] = item
                else:
                    print(f"Item is not a Block: {item}")
        else:
            print(f"Response is not valid or not a list: {response}")
    return known_faces


# Definir le nombre maximum de visages a charger
max_face_id = 10  # Remplacez par le nombre maximum de visages que vous attendez

# Charger les visages connus depuis la carte SD
known_faces = load_known_faces_from_sd(max_face_id)
print(f"Known faces dictionary: {known_faces}")

while True:
    blocks = hl.requestAll()

    for block in blocks:
        if block.learned:
            face_id = block.ID
            if face_id in known_faces:
                print(f"Known Face! ID: {face_id}")
            else:
                print(f"Known Face with unregistered ID: {face_id}")
        else:
            print("Unknown Face!")
        time.sleep(0.5)
    time.sleep(2)
