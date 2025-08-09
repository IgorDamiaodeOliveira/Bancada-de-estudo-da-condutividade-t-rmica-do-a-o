#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 2  // Pino de dados conectado aos sensores

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensores(&oneWire);

DeviceAddress sensor1, sensor2;  // Endereços únicos dos sensores

void setup() {
  Serial.begin(9600);
  sensores.begin();

  Serial.println("Buscando sensores...");

  if (!sensores.getAddress(sensor1, 0)) {
    Serial.println("Sensor 1 não encontrado.");
  }
  if (!sensores.getAddress(sensor2, 1)) {
    Serial.println("Sensor 2 não encontrado.");
  }

  sensores.setResolution(sensor1, 12);
  sensores.setResolution(sensor2, 12);
}

void loop() {
  sensores.requestTemperatures();

  float temp1 = sensores.getTempC(sensor1);
  float temp2 = sensores.getTempC(sensor2);

  Serial.print("Sensor 1: ");
  Serial.print(temp1);
  Serial.println("ºC");

  Serial.print("Sensor 2: ");
  Serial.print(temp2);
  Serial.println("ºC");

  delay(1000);  // 1 segundo entre leituras
}