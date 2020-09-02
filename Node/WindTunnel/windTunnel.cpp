#include "windTunnel.h"

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