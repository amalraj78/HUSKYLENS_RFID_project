import serial
import time

def read_huskylens_data(port):
    try:
        # Initialisation de la connexion série
        ser = serial.Serial(port, 9600, timeout=1)
        time.sleep(2)  # Attendre que la connexion soit établie

        while True:
            # Lire une ligne de données
            data = ser.readline().decode('utf-8').strip()
            if data:
                # Traiter et afficher les données
                print(f"Data from HuskyLens: {data}")

                # Ici, vous pouvez ajouter du code pour traiter les données
                # par exemple, vérifier si le visage est reconnu, etc.

    except serial.SerialException as e:
        print(f"Erreur de connexion au port {port}: {e}")
    except KeyboardInterrupt:
        print("Arrêt du programme")
    finally:
        # Fermer la connexion série
        if ser.is_open:
            ser.close()
            print("Connexion série fermée")

if __name__ == "__main__":
    port = "COM6"  # Remplacez par le port série correct pour votre HuskyLens
    read_huskylens_data(port)
