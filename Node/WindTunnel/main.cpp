#include <Arduino.h>
#include "DPS310.h"
#include "Wire.h"

Dps310 pressure;

#include "adc_ADS114S0.h"
#include "mcp2515.h"

#include "windTunnel.h"

#define EADC_SS 8
#define CAN_SS 9

MCP2515 mcp2515{CAN_SS};
ADS114S0 ads114s0{EADC_SS};

SensorReading readings[] = {};
CANMessage messages[] = {};

void setup()
{
<<<<<<< HEAD
    pinMode(LED_BUILTIN, OUTPUT);
    pressure.begin(Wire);
=======
>>>>>>> 9e38a53... Continued definition of main code using newly created SensorReading and CANMessage classes
}

void loop()
{
    for (uint8_t i = 0; i < sizeof(readings) / sizeof(readings[0]); ++i)
    {
        readings[i].read();
    }

    for (uint8_t i = 0; i < sizeof(messages) / sizeof(messages[0]); ++i)
    {
        messages[i].updateMessageData();
        messages[i].send(&mcp2515);
    }
}
