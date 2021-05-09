#include <Arduino.h>
#include "DPS310.h"
#include "Wire.h"

Dps310 pvtSensor;

void setup()
{
    pinMode(A0, INPUT); //Distance
    pinMode(A1, INPUT); // Distance
    pinMode(A2, INPUT); // Distance
    pinMode(A3, INPUT); // Distance
    pinMode(A11, INPUT); // Diff pressure
    pinMode(A12, INPUT); // Diff pressure
    pinMode(A13, INPUT); // Strain gauge
    pinMode(A7, INPUT); // Strain gauges
    pinMode(A8, INPUT); // Accel x
    pinMode(A9, INPUT); // Accel y
    pinMode(A10, INPUT); // Accel z

    pvtSensor.begin(Wire);
    Serial.begin(9600);
    Wire.begin();
}

void loop()
{
  int distance1, distance2, distance3, distance4 = 0; // distance sensors
  int diff1, diff2 = 0; // Diff pressure sensors
  int amp; // Strain gauge
  int accelX, accelY, accelZ = 0; // Accel
  float pressure, temperature;

  pvtSensor.measureTempOnce(temperature);
  pvtSensor.measurePressureOnce(pressure);
  distance1 = analogRead(A0);
  distance2 = analogRead(A1);
  distance3 = analogRead(A2);
  distance4 = analogRead(A3);
  diff1 = analogRead(A11);
  diff2 = analogRead(A12);
  //Strain guage has a reference pin, so this is subtracted from the output pin to get the true value
  amp = analogRead(A13) - analogRead(A7);
  accelX = analogRead(A8);
  accelY = analogRead(A9);
  accelZ = analogRead(A10);

  Serial.print("Pressure: ");
  Serial.println(pressure);

  Serial.print("Temperature: ");
  Serial.println(temperature);

  Serial.print("Distance sensors: 1: ");
  Serial.print(distance1);
  Serial.print(" 2: ");
  Serial.print(distance2);
  Serial.print(" 3: ");
  Serial.print(distance3);
  Serial.print(" 4: ");
  Serial.println(distance4);

  Serial.print("Differential pressure sensor 1: ");
  Serial.print(diff1);
  Serial.print(" 2: ");
  Serial.println(diff2);

  Serial.print("Strain gauge: ");
  Serial.println(amp);

  Serial.print("Acceleration x: ");
  Serial.print(accelX);
  Serial.print(" y: ");
  Serial.print(accelY);
  Serial.print(" z: ");
  Serial.print(accelZ);
}
