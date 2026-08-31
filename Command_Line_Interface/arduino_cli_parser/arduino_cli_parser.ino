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



  if (Serial.available()) {
    uint8_t cmd = Serial.read();

    mySerial.write(cmd);

    if(cmd>=0 && cmd<14 || cmd >= 91 && cmd <=108 || cmd >= 51 && cmd <= 58 || cmd>= 66 && cmd <= 77 || cmd >= 62 && cmd <= 65 || cmd>= 81 && cmd <= 83){
      // Serial.print("(READ CMD) ");
       if(mySerial.available()){
      // uint8_t cmd = mySerial.read();
      // Serial.println(cmd);
      // Read the incoming bytes until a newline character is found
      String incomingData = mySerial.readStringUntil('\n');
      
      // Trim any trailing carriage returns (\r)
      incomingData.trim();
      
      // Print the received data to the Serial Monitor
      // Serial.print("Received from STM32: ");
      Serial.println(incomingData);
      }
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


