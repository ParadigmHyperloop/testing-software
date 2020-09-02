#include "adc_ADS114S0.h"
#include "can.h"
#include "mcp2515.h"

enum ReadingType
{
    Internal,
    External,
    I2C
};

struct SensorReading
{
    void read();

    ADS114S0* ads114s0; // nullptr if reading is I2C or Internal
    ReadingType type;
    uint8_t address; // Can either be a pin # or an I2C address
    uint16_t data;
};

struct CANMessage
{
    void updateMessageData();
    void send(MCP2515* mcp2515);

    SensorReading* readings[4];
    can_frame frame;
};
