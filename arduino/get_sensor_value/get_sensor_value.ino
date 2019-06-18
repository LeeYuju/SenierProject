uino#include "DHT.h"
#define DHTTYPE DHT11

int dustPin = A0; //Connect dust sensor to Arduino A0 pin
int dustLedPower = 2; //Connect 3 led driver pins of dust sensor to Arduino D2
int DHTPin = 7;
int cdsPin = A1;

String dust = "";
String temperature = "";
String humidity = "";
String light = "";

DHT dht(DHTPin, DHTTYPE);

unsigned long lastMillis = 0;

void setup() {
  Serial.begin(9600);
  pinMode(dustLedPower, OUTPUT);
  dht.begin();
}



void loop() {
  getDhtValue();
  getCdsSensor();
  if (millis() - lastMillis > 10000)
  {
    getDustSensor();
    lastMillis = millis();
    sendSensorValue();
  }
}

void sendSensorValue() {
  Serial.println(makeJsonData());
}


void getDustSensor() {
  float voMeasured = 0;
  float calcVoltage = 0;
  float dustDensity = 0;
  digitalWrite(dustLedPower, LOW); // power on the LED
  delayMicroseconds(280);
  voMeasured = analogRead(dustPin); // read the dust value
  delayMicroseconds(40);
  digitalWrite(dustLedPower, HIGH); // turn the LED off
  delayMicroseconds(9680);

  calcVoltage = voMeasured * (5.0 / 1024.0);
  dustDensity = 0.17 * calcVoltage - 0.1;
  dust = String(dustDensity);
}

void getDhtValue() { //온도, 습도, 가스 센서 값을 수집하는 함수입니다.
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t)) {
    return;
  }
  temperature = String(t);
  humidity = String(h);
}


void getCdsSensor() {
  int cdsInt = analogRead(cdsPin);
  light = String(cdsInt);
}

String makeJsonData() {
  //  {"temperature":0,"humidity":2,"light":3,"dust":4}
  return "{\"temperature\":" + temperature + ",\"humidity\":" + humidity + ",\"light\":" + light + ",\"dust\":" + dust + "}";
}
