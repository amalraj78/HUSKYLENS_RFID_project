import time
import json
from huskylib import HuskyLensLibrary, Block

# Program Parameters
text_on = True
sms_interval = 10
last_sms_time = 0

# Change for your Serial Port
hl = HuskyLensLibrary("SERIAL", "COM6", 3000000)

# Fonction pour récupérer les visages appris
def get_known_faces():
    known_faces = {}
    learned_faces = hl.learnedBlocks()  # Utiliser learnedBlocks() pour obtenir les visages appris
    print(f"Learned faces: {learned_faces}")  # Debug: Impression des visages appris

    # Vérifiez si learned_faces est une instance de Block
    if isinstance(learned_faces, Block):
        known_faces[learned_faces.ID] = learned_faces
    else:
        print("learnedBlocks did not return a single Block instance.")
        
    return known_faces

# Obtenir les visages connus
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
