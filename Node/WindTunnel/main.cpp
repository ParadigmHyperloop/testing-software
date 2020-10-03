#include <Arduino.h>
#include "DPS310.h"
#include "Wire.h"

Dps310 pressure;

void setup()
{
    pinMode(LED_BUILTIN, OUTPUT);
    pressure.begin(Wire);
}

void loop()
{
    digitalWrite(LED_BUILTIN, HIGH);
    delay(1000);
    digitalWrite(LED_BUILTIN, LOW);
    delay(1000);
}
