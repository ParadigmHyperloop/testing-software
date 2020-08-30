#include <Arduino.h>
#include "DPS310.h"
#include "Wire.h"

Dps310 pressure;

#include "adc_ADS114S0.h"
#include "mcp2515.h"

#define EADC_SS 8
#define CAN_SS 9

MCP2515 mcp2515{CAN_SS};
ADS114S0 ads114s0{EADC_SS};

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
