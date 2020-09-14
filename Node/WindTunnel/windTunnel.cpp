#include <Arduino.h>
#include <Wire.h>

#include "adc_ADS114S0.h"
#include "mcp2515.h"

#include "windTunnel.h"

#define EADC_SS 8
#define CAN_SS 9

MCP2515 mcp2515{CAN_SS};
ADS114S0 ads114s0{EADC_SS};

SensorReading readings[] = {};
CANMessage messages[] = {};

void SensorReading::read()
{
    switch (type)
    {
        case Internal:
        {
            data = analogRead(address);
            break;
        }

        case External:
        {
            ads114s0->setMux(static_cast<InputMux>(address));
            data = ads114s0->readData();
            break;
        }

        case I2C:
        {
            // TODO
            break;
        }
    }
}

void CANMessage::updateMessageData()
{
    uint8_t i = 0;
    uint8_t j = 0;
    for (; i < 4; ++i)
    {
        frame.data[j++] = (readings[i]->data & 0xff00) >> 8;
        frame.data[j++] = readings[i]->data & 0x00ff;
    }
}

void CANMessage::send(MCP2515* mcp2515)
{
    mcp2515->sendMessage(&frame);
}

void setup()
{
    Wire.begin();
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
