#include <Wire.h>
#include <SoftwareSerial.h>
#include <MFRC522.h>
#include <RTClib.h> // Bibliothèque pour le module RTC

#define RST_PIN 9
#define SS_PIN 10

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Création d'un objet MFRC522
SoftwareSerial huskySerial(2, 3);   // RX, TX pour la HuskyLens
RTC_DS3231 rtc;                     // Création d'un objet RTC

// Structure pour associer tag et visage
struct User {
  String tagID;
  int faceID;
  String name;
};

// Liste des utilisateurs (à compléter avec vos données)
User users[] = {
  {"0A1B2C3D4E", 1, "Alice"},
  {"1B2C3D4E5F", 2, "Bob"},
  // Ajoutez d'autres utilisateurs ici
};

void setup() {
  Serial.begin(9600);
  SPI.begin();           // Initialisation de la communication SPI
  mfrc522.PCD_Init();    // Initialisation du MFRC522
  huskySerial.begin(9600);
  
  if (!rtc.begin()) {
    Serial.println("RTC non trouvé !");
    while (1);
  }
  if (rtc.lostPower()) {
    Serial.println("Réglage de l'heure par défaut !");
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }
}

void loop() {
  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
    delay(50);
    return;
  }

  String tagID = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    tagID += String(mfrc522.uid.uidByte[i], HEX);
  }

  int faceID = identifyFace();
  
  for (int i = 0; i < sizeof(users) / sizeof(users[0]); i++) {
    if (users[i].tagID == tagID && users[i].faceID == faceID) {
      DateTime now = rtc.now();
      Serial.print("Nom: ");
      Serial.print(users[i].name);
      Serial.print(", Heure d'arrivée: ");
      Serial.println(now.timestamp());
      return;
    }
  }
  
  Serial.println("Erreur : Tag et visage non correspondants !");
}

int identifyFace() {
  huskySerial.write("K"); // Commande HuskyLens pour obtenir l'ID du visage
  delay(100);             // Attente de la réponse

  if (huskySerial.available()) {
    int faceID = huskySerial.parseInt();
    return faceID;
  }
  
  return -1; // Aucune correspondance
}
