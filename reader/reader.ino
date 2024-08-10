#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
MFRC522 mfrc522(SS_PIN, RST_PIN);

#define LED_READY 7
#define LED_SUCCESS 6
#define LED_ERROR 5

String currentTime = "2024-08-10 08:00:00"; // Default time
String status = "ENTRY"; // Default status

void setup() {
    Serial.begin(9600);
    SPI.begin();
    mfrc522.PCD_Init();

    pinMode(LED_READY, OUTPUT);
    pinMode(LED_SUCCESS, OUTPUT);
    pinMode(LED_ERROR, OUTPUT);

    digitalWrite(LED_READY, HIGH); // Ready to scan
}

void loop() {
    if (Serial.available()) {
        String command = Serial.readStringUntil('\n');
        if (command.startsWith("TIME:")) {
            currentTime = command.substring(5); // Extract time from command
        } else if (command.startsWith("STATUS:")) {
            status = command.substring(7); // Extract status from command
        }
    }

    if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
        return;
    }

    digitalWrite(LED_READY, LOW); // Scanning...

    String uid = "";
    for (byte i = 0; i < mfrc522.uid.size; i++) {
        uid += String(mfrc522.uid.uidByte[i], HEX);
    }
    uid.toUpperCase(); // Ensure UID is in uppercase

    // Send UID and current time to Serial
    Serial.println(uid + "," + currentTime + "," + status);

    // Turn on LED_SUCCESS for 1 second
    digitalWrite(LED_SUCCESS, HIGH);
    delay(1000); // Keep LED on for 1 second
    digitalWrite(LED_SUCCESS, LOW);

    mfrc522.PICC_HaltA();
    mfrc522.PCD_StopCrypto1();

    digitalWrite(LED_READY, HIGH);
    delay(1000); // To prevent multiple scans
}
