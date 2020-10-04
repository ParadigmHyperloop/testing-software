#ifndef WINDTUNNEL_H
#define WINDTUNNEL_H

#include <Wire.h>

#include "adc_ADS114S0.h"
#include "can.h"
#include "Dps310.h"
#include "mcp2515.h"

enum ReadingType
{
    Internal,
    External
};

class PressureSensor
{
public:
    void measurePressure();
    float& getResult(){ return m_result; } 

private:
    Dps310 m_dps310;
    float m_result;
};

class SensorReading
{
public:
    void read();
    void begin();
    uint16_t getData(){ return m_data; }

private:
    ADS114S0* m_ads114s0; // nullptr if reading is I2C or Internal
    ReadingType m_type;
    uint8_t m_address; // Can either be a pin # or an I2C address
    uint16_t m_data;
};

class CANMessage
{
public:
    void updateMessageData();
    void send(MCP2515* mcp2515);

private:
    SensorReading* m_srReadings[4];
    PressureSensor* m_pReadings[2];
    can_frame frame;
};

#endif // WINDTUNNEL_H