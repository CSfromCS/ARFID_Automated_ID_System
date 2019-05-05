#include <GSM.h>
#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN          10         // Configurable, see typical pin layout above
#define RST_PIN         9          // Configurable, see typical pin layout above

int led = 5;
int buzzer = 4;

char choice[1];
byte nuidPICC[4];

bool rfidReady = false;
bool gsmReady = false;
MFRC522 rfid(SS_PIN, RST_PIN);  // Create MFRC522 instance
MFRC522::MIFARE_Key key; 


#define PINNUMBER "1234"
GSM gsmAccess;
GSM_SMS sms;

void setup() {
  pinMode(led, OUTPUT);
  pinMode(buzzer, OUTPUT);
  Serial.begin(9600);   // Initialize serial communications with the PC
  Serial.println("Input: ");
}

void loop() {
  readSerial(choice);
  switch(choice[0]){
    case '0':
      restartArduino();
      break;
    case '1':
      checkRfidScanner();
      break;
    case '2':
      initGsm();
      break;
    case '3':
      if(rfidReady){
        Serial.println("Scanning...");
        scanning();
      }else
        Serial.println("Initialize RFID scanner first.");
      break;
    case '4':
      if(gsmReady)
        sendMessage();
      else
        Serial.println("Initialize GSM scanner first.");
      break;
    default:
      Serial.println(" ");    
  }
}

//void initRfid(){
//  rfid.PCD_Init();   // Init MFRC522 module
//  rfidReady = true;
//  Serial.println("Done.");
//}

void initGsm(){
  while (!gsmReady) {
      Serial.println("Trying to connect...");
    if (gsmAccess.begin(PINNUMBER) == GSM_READY) {
      gsmReady = true;
      Serial.println("Ready.");
    }else{
      Serial.println("Not connected, retrying...");
      delay(1000);
    }
  }
  Serial.println("GSM initialized");
  Serial.println("Done.");
}

void checkRfidScanner(){
  SPI.begin();          // Init SPI bus
  bool result = rfid.PCD_PerformSelfTest(); // perform the test
  if (result){
    rfidReady = true;
    Serial.println("Ready.");
  }else{
    rfidReady = false;
    Serial.println("Failed.");
  }
  rfid.PCD_Init();   // Init MFRC522 module
  for (byte i = 0; i < 6; i++) {
    key.keyByte[i] = 0xFF;
  }
  Serial.println("Done.");
}

void scanning(){
  if (Serial.available() > 0) {
    char exit = Serial.read();
    if(exit == 'x'){
      Serial.println("Done.");
      return;
    }
  }
  scanOnce();
  delay(200);
  
  digitalWrite(led, LOW);
  digitalWrite(buzzer, LOW);
  
  scanning();
}

void scanOnce(){
  // Look for new cards
  if (!rfid.PICC_IsNewCardPresent())
    return;

  // Verify if the UID has been read
  if (!rfid.PICC_ReadCardSerial())
    return;

  digitalWrite(led, HIGH);
  digitalWrite(buzzer, HIGH);
  
  for (byte i = 0; i < 4; i++) {
    nuidPICC[i] = rfid.uid.uidByte[i];
  }

  Serial.print("UID:");
  printHex(rfid.uid.uidByte, rfid.uid.size);
  Serial.println();
  
  rfid.PICC_HaltA();

  rfid.PCD_StopCrypto1();
}

void printHex(byte *buffer, byte bufferSize) {
  
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
}

//void checkSimNetwork(){
//  return;
//}

int readSerial(char result[]) {
  int i = 0;
  while (1) {
    while (Serial.available() > 0) {
      char inChar = Serial.read();
      if (inChar == '\n') {
        result[i] = '\0';
        Serial.flush();
        return 0;
      }
      if (inChar != '\r') {
        result[i] = inChar;
        i++;
      }
    }
  }
}
void sendMessage(){
  
  char remoteNum[20];  // telephone number to send sms
  Serial.print("Number: ");
  readSerial(remoteNum);
  Serial.println(remoteNum);

  // sms text
  char txtMsg[200];
  Serial.print("Message: ");
  readSerial(txtMsg);
  Serial.println(txtMsg);

  // send the message
  sms.beginSMS(remoteNum);
  sms.print(txtMsg);
  sms.endSMS();
  Serial.println("COMPLETE!");
  Serial.println("Done.");
}

void(* resetFunc) (void) = 0;
void restartArduino(){
  Serial.println("Restarting...");
  delay(50);
  resetFunc();
}
