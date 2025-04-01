
#https://www.hackster.io/AlexWulff/ai-intruder-detection-system-with-huskylens-98e636
import time
from huskylib import HuskyLensLibrary, Block

# Change for your Serial Port
hl = HuskyLensLibrary("SERIAL", "/dev/ttyUSB0", 3000000)

# Dictionnaire pour associer les IDs aux noms
face_names = {
    1: "Alice",
    2: "Bob",
    3: "Charlie",
    # Ajoutez d'autres IDs et noms ici
}

while True:
    blocks = hl.requestAll()

    for block in blocks:
        if block.learned:
            face_id = block.ID
            face_name = face_names.get(face_id, "Unknown Face")
            print(f"Known Face! ID: {face_id}, Name: {face_name}")

            hl.customText(face_name, block.x, block.y)
        else:
            print("Unknown Face!")
            hl.clearText()
        time.sleep(0.5)
    time.sleep(2)
