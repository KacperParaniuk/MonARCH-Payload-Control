int incomingByte = 0; // for incoming serial data

#include <SoftwareSerial.h>



const byte rxPin = 2;  // RX of the device
const byte txPin = 3;  // TX of the device

SoftwareSerial mySerial(rxPin, txPin);  

#define LED_1 13



void setup() {
  Serial.begin(115200);      // For Serial Monitor
  mySerial.begin(9600);    // For STM32 (use lower baud like 9600 if issues)


  pinMode(LED_1, OUTPUT);


}

void loop() {

  // uint8_t cmd = 78;

  // mySerial.write(cmd);  // need write to print the raw binary value

  // // Serial.print(78);

//  delay(1000);

//   digitalWrite(LED_1, 1);

//   delay(200);

//   digitalWrite(LED_1,0);



  if (Serial.available() >= 2) {
    uint8_t cmd = Serial.read();
    uint8_t arg = Serial.read();


    mySerial.write(cmd);
    mySerial.write(arg);


    // wait for STM32 to respond
    unsigned long start = millis();
    while (!mySerial.available() && millis() - start < 3000) {
        delay(1); 
    }

    if (mySerial.available()) {
        String incomingData = mySerial.readStringUntil('\n');
        incomingData.trim();
        Serial.println(incomingData);
    }

    digitalWrite(LED_1, 1);
    delay(100);
    digitalWrite(LED_1, 0);
    delay(100);
    digitalWrite(LED_1, 1);
    delay(100);
    digitalWrite(LED_1, 0);
    delay(100);

    }
    else{
    delay(500);
    digitalWrite(LED_1, 0);

    }

//     delay(500);

  
}


