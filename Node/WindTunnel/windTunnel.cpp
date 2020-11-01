#include <Arduino.h>
#include <Wire.h>

#include "adc_ADS114S0.h"
#include "mcp2515.h"

#include "windTunnel.h"

#define EADC_SS 8
#define CAN_SS 9

MCP2515 CanBus{CAN_SS};
ADS114S0 EADC{EADC_SS};

void PressureSensor::measurePressure()
{
    m_dps310.measurePressureOnce(m_result);
}

void SensorReading::read()
{
    switch (m_type)
    {
        case Internal:
        {
            m_data = analogRead(m_address);
            break;
        }

        case External:
        {
            m_ads114s0->setMux(static_cast<InputMux>(m_address));
            m_data = m_ads114s0->readData();
            break;
        }
    }
}

void CANMessage::updateMessageData()
{
    if (m_srReadings)
    {
        uint8_t i = 0;
        uint8_t j = 0;
        for (; i < 4; ++i)
        {
            frame.data[j++] = (m_srReadings[i]->getData() & 0xff00) >> 8;
            frame.data[j++] = m_srReadings[i]->getData() & 0x00ff;
        }
    }
    else // Pressure Reading
    {
        // Have to pack 2 32-bit floats into and array of 8 unsigned ints
        // Using memcpy circumvents the typing, and allows this to be possible
        memcpy(frame.data, &(m_pReadings[1]->getResult()), sizeof(float));
        memcpy(frame.data + 4, &(m_pReadings[0]->getResult()), sizeof(float));
    }
}

void CANMessage::send(MCP2515* bus)
{
    bus->sendMessage(&frame);
}
