import serial
import time

def test_huskylens_connection(port):
    try:
        print("Initializing serial connection...")
        ser = serial.Serial(port, 9600, timeout=1)
        time.sleep(2)  # Attendre que la connexion soit établie

        if ser.is_open:
            print(f"Connected to {port} at 9600 baud.")
            # Envoyer une commande simple pour vérifier la réponse
            ser.write(b'\x55\xAA\x11\x00\x00')  # Commande pour obtenir l'ID de l'appareil (à vérifier dans la doc HuskyLens)
            time.sleep(1)
            response = ser.read_all()
            print(f"Response from HuskyLens: {response}")

        ser.close()

    except serial.SerialException as e:
        print(f"Erreur de connexion au port {port}: {e}")
    except KeyboardInterrupt:
        print("Arrêt du programme")
    finally:
        if ser.is_open:
            ser.close()
            print("Connexion série fermée")

if __name__ == "__main__":
    port = "COM6"  # Remplacez par le port série correct pour votre HuskyLens
    test_huskylens_connection(port)
