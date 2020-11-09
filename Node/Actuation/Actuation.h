#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include <mcp2515.h>

// TODO class wrapping watchdog timer and heartbeat can message

class ActuationManager
{
public:
    ActuationManager(TwoWire*, MCP2515*);

    bool receiveCommand();

private:
    enum ECommandResponse : uint8_t
    {
        eHeartbeat = 10,
        eInitCommand = 12,
        eInitResponse = 14,
        eSpeedCommand = 16,
        eSpeedResponse = 18,
        eStepCommand = 20,
        eStepResponse = 22
    };

    struct StepperCommand
    {
        uint16_t nSteps;
        uint8_t u8Direction;
        uint8_t u8Style;
    };

    bool InitStepper(uint16_t, uint8_t);
    bool sendInitStepperResponse(uint16_t, uint8_t);

    bool setStepperSpeed(uint16_t, uint8_t);
    bool sendStepperSpeedResponse(uint16_t, uint8_t);

    bool stepperCommand(StepperCommand, uint8_t);
    bool stepperResponse(StepperCommand, uint8_t);

    bool sendHeartbeat();

    bool sendResponse();

    TwoWire* m_pI2C;
    MCP2515* m_can;
    Adafruit_MotorShield m_motorShield;
    Adafruit_StepperMotor* m_apSteppers[2];
};

