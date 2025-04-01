import time
import json
from huskylib import HuskyLensLibrary


# Change for your Serial Port
hl = HuskyLensLibrary("SERIAL", "COM6", 3000000)

# Fonction pour récupérer les visages appris
def get_known_faces():
    learned_faces = hl.learnedBlocks()
    known_faces = {}
    for face in learned_faces:
        known_faces[face.ID] = face
    return known_faces

known_faces = get_known_faces()

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
