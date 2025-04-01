import time
import json
from huskylib import HuskyLensLibrary, Block

# Program Parameters
max_face_id=5

# Change for your Serial Port
hl = HuskyLensLibrary("SERIAL", "/dev/ttyUSB0", 3000000)

# Fonction pour rcuprer les visages appris
def get_known_faces():
    known_faces = {}
    learned_face = hl.learnedBlocks()  # Utiliser learnedBlocks() pour obtenir le visage appris
    print(f"Learned faces: {learned_face}")  # Debug: Impression des visages appris

    # Vrifiez si learned_face est une instance de Block
    if isinstance(learned_face, Block):
        known_faces[learned_face.ID] = learned_face
    else:
        print("learnedBlocks did not return a Block instance.")
        
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
