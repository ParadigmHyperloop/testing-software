#include "Actuation.h"

ActuationManager::ActuationManager(TwoWire* pI2C, const uint8_t u8Cs)
    : m_pI2C(pI2C), m_can(u8Cs), m_motorShield()
{}

bool ActuationManager::receiveCommand()
{
    bool bStatus;
    can_frame frame = {0};
    MCP2515::ERROR response = m_can.readMessage(&frame);
    if (response != MCP2515::ERROR_OK)
    {
        return false;
    }
    switch (frame.can_id)
    {
        case (eInitCommand):
        {
            uint16_t u16Data = (frame.data[0] << 8) | frame.data[1];
            uint8_t u8Address = frame.data[2];
            bStatus = InitStepper(u16Data, u8Address);
            break;
        }
        case (eSpeedCommand):
        {
            uint16_t u16Data = (frame.data[0] << 8) | frame.data[1];
            uint8_t u8Address = frame.data[2];
            bStatus = setStepperSpeed(u16Data, u8Address);
            break;
        }
        case (eStepCommand):
        {
            StepperCommand command = {
                (frame.data[0] << 8) | frame.data[1],
                frame.data[2],
                frame.data[3]
            };
            bStatus = stepperCommand(command, frame.data[4]);
            break;
        }
    }

    return bStatus;
}

bool ActuationManager::InitStepper(uint16_t u16Step, uint8_t u8Address)
{
    if (u8Address != 1 || u8Address != 2)
    {
        return false;
    }
    if (m_apSteppers[u8Address - 1] == nullptr)
    {
        m_apSteppers[u8Address - 1] = m_motorShield.getStepper(u16Step, u8Address);
    }
    return sendInitStepperResponse(u16Step, u8Address);
}

bool ActuationManager::sendInitStepperResponse(uint16_t u16Step, uint8_t u8Address)
{
    uint8_t au8Data[] = { (uint8_t)((u16Step & 0xFF00) >> 8), (uint8_t)(u16Step & 0x00FF), u8Address };
    uint8_t au8IdBuf[4];
    m_can.prepareId(au8IdBuf, false, eInitResponse);

    can_frame frame = { &au8IdBuf, 8, au8Data };

    MCP2515::ERROR status = m_can.sendMessage(&frame);
    if (status != MCP2515::ERROR_OK)
    {
        return false;
    }
    
    return true;
}

bool ActuationManager::setStepperSpeed(uint16_t u16Speed, uint8_t u8Address)
{
    if (m_apSteppers[u8Address - 1] == nullptr)
    {
        return false;
    }
    m_apSteppers[u8Address - 1]->setSpeed(u16Speed);

    return sendStepperSpeedResponse(u16Speed, u8Address);
}

bool ActuationManager::sendStepperSpeedResponse(uint16_t u16Speed, uint8_t u8Address)
{
    uint8_t au8Data[] = { (uint8_t)((u16Speed & 0xFF00) >> 8), (uint8_t)(u16Speed & 0x00FF), u8Address };
    uint8_t au8IdBuf[4];
    m_can.prepareId(au8IdBuf, false, eSpeedResponse);

    can_frame frame = { &au8IdBuf, 8, au8Data };

    MCP2515::ERROR status = m_can.sendMessage(&frame);
    if (status != MCP2515::ERROR_OK)
    {
        return false;
    }

    return true;
}

bool ActuationManager::stepperCommand(StepperCommand command, uint8_t u8Address)
{
    if (m_apSteppers[u8Address - 1] == nullptr)
    {
        return false;
    }
    m_apSteppers[u8Address - 1]->step(command.nSteps, command.u8Direction, command.u8Style);

    return stepperResponse(command, u8Address);
}

bool ActuationManager::stepperResponse(StepperCommand command, uint8_t u8Address)
{
    uint8_t au8Data[] = {
        (uint8_t)((command.nSteps & 0xFF00) >> 8),
        (uint8_t)(command.nSteps & 0x00FF),
        command.u8Direction,
        command.u8Style,
        u8Address
    };
    uint8_t au8IdBuf[4];
    m_can.prepareId(au8IdBuf, false, eStepResponse);

    can_frame frame = { &au8IdBuf, 8, au8Data };

    MCP2515::ERROR status = m_can.sendMessage(&frame);
    if (status != MCP2515::ERROR_OK)
    {
        return false;
    }

    return true;
}

bool ActuationManager::sendHeartbeat()
{
    uint8_t au8IdBuf[4];
    m_can.prepareId(au8IdBuf, false, eHeartbeat);
    can_frame frame = {0};

    frame.can_id = &au8IdBuf;

    MCP2515::ERROR status = m_can.sendMessage(&frame);
    if (status != MCP2515::ERROR_OK)
    {
        return false;
    }

    return true;
}

int main(void)
{
    ActuationManager manager{&Wire, 15};
    return 0;
}

