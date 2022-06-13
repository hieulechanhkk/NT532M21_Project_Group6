#include <LoRa.h>
#include <SoftwareSerial.h>
#include <DHT.h>
SoftwareSerial loraSerial(12, 13); //RX,TX;

const int DHTPIN = 14;      
const int DHTTYPE = DHT22;  
DHT dht(DHTPIN, DHTTYPE);

const int M0 = 4 ;   // M0 de set up MODE cho Module Lora
const int M1 = 5 ;   // M1 de set up MODE cho Module Lora
String fire = "";

String Area = "Khu Vuc A";
void setup() {
  // thiết lập pin cho sensor đo độ ẩm
 pinMode(A0, INPUT);
 pinMode(M0,OUTPUT);
 pinMode(M1, OUTPUT);
 digitalWrite(M0,LOW);
 digitalWrite(M1,HIGH);

  Serial.begin(9600); 
  loraSerial.begin(9600);
  dht.begin();
}

void loop() {
   if (Serial.available() ) { 
      fire= Serial.read();
   }
   long humi= dht.readTemperature();
   long temper = dht.readHumidity();
  
   String data = Area + "/" + String(humi) + "/" + String(temper) + "/" + fire;
  //gửi thông tin độ ẩm đất đến lora gateway
  loraSerial.print(data);
  delay(7000);
}
