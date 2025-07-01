import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from huskylib import HuskyLensLibrary

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

LED_true=5
LED_false=7

GPIO.setup(LED_true, GPIO.OUT)
GPIO.setup(LED_false, GPIO.OUT)

GPIO.output(LED_true, GPIO.LOW)
GPIO.output(LED_false, GPIO.LOW)   


# Initialisation du lecteur RFID
reader = SimpleMFRC522()

# Initialisation du HuskyLens
hl = HuskyLensLibrary("SERIAL", "/dev/ttyUSB0", 3000000)

# Dictionnaires pour associer les IDs de visage aux noms et les IDs de tags RFID aux IDs de visage
face_names = {}
rfid_to_face_id = {}

def read_rfid():
    GPIO.output(LED_true, GPIO.LOW)
    GPIO.output(LED_false, GPIO.LOW)
    print("Scannez votre tag RFID...")
    attempts = 3
    while attempts > 0:
        try:
            id, text = reader.read()
            print(f"ID du tag RFID: {id}")
            return id
        except Exception as e:
            print(f"Erreur lors de la lecture du tag RFID: {e}")
            attempts -= 1
            time.sleep(1)
    print("Echec de la lecture du tag RFID après plusieurs tentatives.")
    return None

def recognize_face(expected_face_id=None):
    GPIO.output(LED_true, GPIO.LOW)
    GPIO.output(LED_false, GPIO.LOW)
    print("Veuillez montrer votre visage")
    while True:
        blocks = hl.requestAll()
        for block in blocks:
            if block.learned:
                face_id = block.ID
                if expected_face_id is None or face_id == expected_face_id:
                    face_name = face_names.get(face_id, "Visage inconnu")
                    print(f"Visage connu! ID: {face_id}, Nom: {face_name}")
                    GPIO.output(LED_true, GPIO.HIGH)
                    GPIO.output(LED_false, GPIO.LOW)
                    return face_id
                else:
                    print("Le visage ne correspond pas avec le tag RFID attendu")
                    GPIO.output(LED_true, GPIO.LOW)
                    GPIO.output(LED_false, GPIO.HIGH)
            else:
                print("Visage inconnu!")
                GPIO.output(LED_true, GPIO.LOW)
                GPIO.output(LED_false, GPIO.HIGH)
        time.sleep(1)


def register_user(name):
    global face_names, rfid_to_face_id
    
    rfid_id = read_rfid()
    if rfid_id is None:
        return None
    
    face_id = recognize_face()
    
    face_names[face_id] = name
    rfid_to_face_id[rfid_id] = face_id
    
    return face_id


def recognize_user():
    global face_names, rfid_to_face_id
    
    rfid_id = read_rfid()
    if rfid_id is None:
        return None
    
    if rfid_id in rfid_to_face_id:
        associated_face_id = rfid_to_face_id[rfid_id]
        print(f"Veuillez montrer votre visage: {associated_face_id}")
        recognized_face_id = recognize_face(associated_face_id)
        if recognized_face_id is not None:
            return recognized_face_id
        else:
            return None
    else:
        return None



def cleanup():
    GPIO.cleanup()
