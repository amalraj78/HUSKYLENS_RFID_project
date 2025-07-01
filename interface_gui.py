import tkinter as tk
from tkinter import messagebox
from tkinter import *
from datetime import datetime
import RPi.GPIO as GPIO
import time
import reconnaissance  # Importation du module de reconnaissance

#Réglage des GPIO


def register_user_window():
    register_window = tk.Toplevel(root)
    register_window.title("Enregistrer un nouvel utilisateur")

    instructions = tk.Label(register_window, text="Scannez votre tag RFID et montrez votre visage à la caméra.")
    instructions.pack(pady=10)

    name_label = tk.Label(register_window, text="Entrez votre nom:")
    name_label.pack(pady=5)
    name_entry = tk.Entry(register_window)
    name_entry.pack(pady=5)

    def register():
        name = name_entry.get()
        if not name:
            messagebox.showerror("Erreur", "Le nom ne peut pas etre vide.")
            return
        
        face_id = reconnaissance.register_user(name)
        if face_id is not None:
            messagebox.showinfo("Succès", f"Utilisateur {name} enregistré avec succès.")
            register_window.destroy()

        else:
            messagebox.showerror("Erreur", "échec de l'enregistrement de l'utilisateur.")

    register_button = tk.Button(register_window, text="Enregistrer", command=register)
    register_button.pack(pady=20)


def recognize_user_window():
    recognized_face_id = reconnaissance.recognize_user()
    if recognized_face_id is not None:
        face_name = reconnaissance.face_names.get(recognized_face_id, "Visage inconnu")
        recognized_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        show_recognition_result(face_name, recognized_time)
               

def show_recognition_result(face_name, recognized_time):
    # Fonction pour afficher la nouvelle fenetre avec les détails de reconnaissance
    window = tk.Toplevel(root)
    window.title("Résultat de Reconnaissance Faciale")

    # Création des étiquettes pour afficher les informations
    tk.Label(window, text=f"Nom: {face_name}").pack()
    tk.Label(window, text=f"Heure de Reconnaissance: {recognized_time}").pack()



# Configuration de l'interface graphique Tkinter
root = tk.Tk()
root.geometry("1920x1080")

root.title("RFID Face Recognition")

register_button = tk.Button(root, text="Enregistrer Tag/Visage/Nom", command=register_user_window)
register_button.pack(pady=10)

recognize_button = tk.Button(root, text="Authentification", command=recognize_user_window)
recognize_button.pack(pady=10)

quit_button = tk.Button(root, text="Quitter", command=root.quit)
quit_button.pack(pady=10)



root.mainloop()

# Nettoyage des GPIO a la sortie de l'application
reconnaissance.cleanup()
