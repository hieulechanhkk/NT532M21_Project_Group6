#include <ESP8266WiFi.h>   
#include <ArduinoJson.h>
#include<WiFiClient.h>
#include <ESP8266HTTPClient.h>
#include <Wire.h>
#include <BH1750.h>
#include <Arduino_JSON.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
SoftwareSerial loraSerial(D3, D2); //RX,TX;
const char* ssid = "UiTiOt-E3.1";
const char* password =  "UiTiOtAP";

String API = "http://lab3-iot-nodejs.herokuapp.com/v1";

String fire = "";
String area = "";
int temp  = 0;
int hum = 0;
WiFiClient espClient;
WiFiClient httpClient = espClient;
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "1.vn.pool.ntp.org");
#define LED LED_BUILTIN
void setup() {
  pinMode(D4, OUTPUT);
  pinMode(D5, OUTPUT);
  Serial.begin(115200);
  pinMode(LED, OUTPUT);
  WiFi.begin(ssid, password); 
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }
 
  Serial.println("Connected to the WiFi network");
  loraSerial.print(humiData);

}


void post_to_api(long temp, long hum, String detect){
  if(WiFi.status()== WL_CONNECTED){
 
   HTTPClient http;
   String apifinal = "http://lab3-iot-nodejs.herokuapp.com/v1/data/62a32f752e2af3c7e39ab290";
   http.begin(httpClient,apifinal);  
   http.addHeader("Content-Type", "application/json");          
   StaticJsonDocument<200> doc;
   doc["_id"] = "62a32f752e2af3c7e39ab290";
   doc["temperature"] = temp;
   doc["humidity"] = hum;
   doc["detect"] = detect;
   String requestBody;
    serializeJson(doc, requestBody);
   int httpResponseCode = http.PUT(requestBody);   
    
   if(httpResponseCode>0){
 
    String response = http.getString(); 
    Serial.println(response);  
   }else{
 
    Serial.print("Error on sending PUT Request: ");
    Serial.println(httpResponseCode);
 
   }
 
  http.end();
  }else{
    Serial.println("Error in WiFi connection");
  }
}
void xuly(String result) {
  int i;
  char delimiter[] = "/";
  char *p;
  char string[128];
  String words[4];

  result.toCharArray(string, sizeof(string));
  i = 0;
  p = strtok(string, delimiter);
  while(p && i < 4)
  {
    words[i] = p;
    p = strtok(NULL, delimiter);
    ++i;
  }
  area = words[0];
  temp = words[1].toInt();
  hum = words[2].toInt();
  fire = words[3];
}


void post_temp_to_log(long temp, long hum, String detect)
{
  if(WiFi.status()== WL_CONNECTED){
 
   HTTPClient http;
   String apifinal = "http://lab3-iot-nodejs.herokuapp.com/v1/log";
   http.begin(httpClient,apifinal);  
   http.addHeader("Content-Type", "application/json");          
   StaticJsonDocument<200> doc;
   StaticJsonDocument<200> doc1;
   doc["area"] = area;
   doc["temperature"] = temp;
   doc["humidity"] = hum;
   doc["detect"] = detect;
   String requestBody;
    serializeJson(doc, requestBody);
   int httpResponseCode = http.POST(requestBody);
   http.end();
  }
}
void loop() {
  String message = loraSerial.readString();
  xuly(message);
  post_to_api(temp, hum, fire);
  post_temp_to_log(temp, hum, fire);
  delay(100);
}
