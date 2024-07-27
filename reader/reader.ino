#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9

MFRC522 mfrc522(SS_PIN, RST_PIN);

#define WHITE_LED 5
#define GREEN_LED 6
#define RED_LED 7

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  
  pinMode(WHITE_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  
  digitalWrite(WHITE_LED, HIGH);  // Indicate ready to tap
  digitalWrite(GREEN_LED, LOW);
  digitalWrite(RED_LED, LOW);
}

void loop() {
  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  digitalWrite(WHITE_LED, LOW);  // Turn off ready LED

  String uidString = "";
  Serial.print("UID: ");
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    uidString += String(mfrc522.uid.uidByte[i], HEX);
    Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? "0" : ""); // Leading zero for single digit
    Serial.print(mfrc522.uid.uidByte[i], HEX);
    Serial.print(" ");
  }
  Serial.println();

  if (isValidUID(uidString)) {
    digitalWrite(GREEN_LED, HIGH);  // Success
    delay(1000);  // Hold for 1 second
    digitalWrite(GREEN_LED, LOW);
  } else {
    digitalWrite(RED_LED, HIGH);  // Error
    delay(1000);  // Hold for 1 second
    digitalWrite(RED_LED, LOW);
  }

  digitalWrite(WHITE_LED, HIGH);  // Ready for next tap
}

bool isValidUID(String uid) {
  // Placeholder for UID validation logic
  // Replace with actual logic
  return uid.length() > 0;
}
