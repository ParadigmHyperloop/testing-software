#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include <mcp2515.h>


class ActuationManager
{
public:
    ActuationManager(TwoWire*, const uint8_t);

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

    void InitStepper(uint16_t, uint8_t);
    void sendInitStepperResponse(uint16_t, uint8_t);

    void setStepperSpeed(uint16_t, uint8_t);
    void sendStepperSpeedResponse(uint16_t, uint8_t);

    void stepperCommand(StepperCommand, uint8_t);
    void stepperResponse(StepperCommand, uint8_t);

    TwoWire* m_pI2C;
    MCP2515 m_can;
    Adafruit_MotorShield m_motorShield;
    Adafruit_StepperMotor* m_apSteppers[2];
};

