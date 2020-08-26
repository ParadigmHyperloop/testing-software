#include <Arduino.h>

#include "adc_ADS114S0.h"
#include "mcp2515.h"

#define EADC_SS 7
#define CAN_SS 18

MCP2515 mcp2515{CAN_SS};
ADS114S0 ads114s0{EADC_SS};

void setup()
{
    pinMode(PIN_SPI_SS, OUTPUT);
    pinMode(A0, INPUT);

    ads114s0.reset();
    ads114s0.setMux(MUX_SINGLE_0);
}

void loop()
{
    uint16_t internalReading = analogRead(A0);
    uint16_t externalReading = ads114s0.readData();

    Serial.println(internalReading);
    Serial.println(externalReading);

    can_frame internalMessage = { 200, 2, { (uint8_t)((internalReading & 0xff00) >> 8), (uint8_t)(internalReading & 0x00ff) } };
    can_frame externalMessage = { 201, 2, { (uint8_t)((externalReading & 0xff00) >> 8), (uint8_t)(externalReading & 0x00ff) } };

    mcp2515.sendMessage(&internalMessage);
    mcp2515.sendMessage(&externalMessage);
}
