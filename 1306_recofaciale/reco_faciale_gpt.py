#import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import serial
from datetime import datetime

# Configuration du lecteur RFID RC522
reader = SimpleMFRC522()


husky_serial = serial.Serial('/dev/ttyS0', 9600, timeout=1)

# Structure pour associer tag et visage
users = {
    "0A1B2C3D4E": {"faceID": 1, "name": "Alice"},
    "1B2C3D4E5F": {"faceID": 2, "name": "Bob"},
    # Ajoutez d'autres utilisateurs ici
}

def identify_face():
    husky_serial.write(b'K')  # Commande HuskyLens pour obtenir l'ID du visage
    line = husky_serial.readline().decode('utf-8').strip()
    if line.isdigit():
        return int(line)
    return -1

def main():
    try:
        while True:
            print("Veuillez passer votre tag RFID...")
            tag_id, text = reader.read()
            tag_id = format(tag_id, 'X')  # Conversion en format hexadécimal

            face_id = identify_face()
            print(f"Tag ID: {tag_id}, Face ID: {face_id}")

            if tag_id in users and users[tag_id]["faceID"] == face_id:
                now = datetime.now()
                print(f"Nom: {users[tag_id]['name']}, Heure d'arrivée: {now}")
            else:
                print("Erreur : Tag et visage non correspondants !")
    except KeyboardInterrupt:
        #GPIO.cleanup()
        print("Programme terminé.")

if __name__ == "__main__":
    main()
