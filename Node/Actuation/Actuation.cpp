#include "Actuation.h"

ActuationManager::ActuationManager(TwoWire* pI2C, MCP2515* can)
    : m_pI2C(pI2C), m_can(can), m_motorShield()
{}

MCP2515::ERROR ActuationManager::receiveCommand(can_frame* frame)
{
    return m_can->readMessage(frame);
}

MCP2515::ERROR ActuationManager::handleCommand(can_frame* frame)
{
    MCP2515::ERROR status;
    switch (frame->can_id)
    {
        case (eInitCommand):
        {
            uint16_t u16Data = (frame->data[0] << 8) | frame->data[1];
            uint8_t u8Address = frame->data[2];
            status = InitStepper(u16Data, u8Address);
            break;
        }
        case (eSpeedCommand):
        {
            uint16_t u16Data = (frame->data[0] << 8) | frame->data[1];
            uint8_t u8Address = frame->data[2];
            status = setStepperSpeed(u16Data, u8Address);
            break;
        }
        case (eStepCommand):
        {
            StepperCommand command = {
                static_cast<uint16_t>((frame->data[0] << 8) | frame->data[1]),
                frame->data[2],
                frame->data[3]
            };
            status = stepperCommand(command, frame->data[4]);
            break;
        }
    }

    return status;
}

MCP2515::ERROR ActuationManager::InitStepper(uint16_t u16Step, uint8_t u8Address)
{
    if (u8Address != 1 || u8Address != 2)
    {
        return MCP2515::ERROR_FAIL;
    }
    if (m_apSteppers[u8Address - 1] == nullptr)
    {
        m_apSteppers[u8Address - 1] = m_motorShield.getStepper(u16Step, u8Address);
    }
    return sendInitStepperResponse(u16Step, u8Address);
}

MCP2515::ERROR ActuationManager::sendInitStepperResponse(uint16_t u16Step, uint8_t u8Address)
{
    uint8_t au8Data[] = { (uint8_t)((u16Step & 0xFF00) >> 8), (uint8_t)(u16Step & 0x00FF), u8Address };
    uint8_t au8IdBuf[4];
    m_can->prepareId(au8IdBuf, false, eInitResponse);

    canid_t* pIdBuf = (canid_t*)au8IdBuf;
    can_frame frame = { *pIdBuf, 8, *au8Data };

    return m_can->sendMessage(&frame);
}

MCP2515::ERROR ActuationManager::setStepperSpeed(uint16_t u16Speed, uint8_t u8Address)
{
    if (m_apSteppers[u8Address - 1] == nullptr)
    {
        return MCP2515::ERROR_FAIL;
    }
    m_apSteppers[u8Address - 1]->setSpeed(u16Speed);

    return sendStepperSpeedResponse(u16Speed, u8Address);
}

MCP2515::ERROR ActuationManager::sendStepperSpeedResponse(uint16_t u16Speed, uint8_t u8Address)
{
    uint8_t au8Data[] = { (uint8_t)((u16Speed & 0xFF00) >> 8), (uint8_t)(u16Speed & 0x00FF), u8Address };
    uint8_t au8IdBuf[4];
    m_can->prepareId(au8IdBuf, false, eSpeedResponse);
    
    canid_t* pIdBuf = (canid_t*)au8IdBuf;
    can_frame frame = { *pIdBuf, 8, *au8Data };

    return m_can->sendMessage(&frame);
}

MCP2515::ERROR ActuationManager::stepperCommand(StepperCommand command, uint8_t u8Address)
{
    if (m_apSteppers[u8Address - 1] == nullptr)
    {
        return MCP2515::ERROR_FAIL;
    }
    m_apSteppers[u8Address - 1]->step(command.nSteps, command.u8Direction, command.u8Style);

    return stepperResponse(command, u8Address);
}

MCP2515::ERROR ActuationManager::stepperResponse(StepperCommand command, uint8_t u8Address)
{
    uint8_t au8Data[] = {
        (uint8_t)((command.nSteps & 0xFF00) >> 8),
        (uint8_t)(command.nSteps & 0x00FF),
        command.u8Direction,
        command.u8Style,
        u8Address
    };
    uint8_t au8IdBuf[4];
    m_can->prepareId(au8IdBuf, false, eStepResponse);

    canid_t* pIdBuf = (canid_t*)au8IdBuf;
    can_frame frame = { *pIdBuf, 8, *au8Data };

    return m_can->sendMessage(&frame);
}

MCP2515::ERROR ActuationManager::sendHeartbeat()
{
    uint8_t au8IdBuf[4];
    m_can->prepareId(au8IdBuf, false, eHeartbeat);
    can_frame frame = {0};

    canid_t* pIdBuf = (canid_t*)au8IdBuf;
    frame.can_id = *pIdBuf;

    return m_can->sendMessage(&frame);
}

int main(void)
{
    MCP2515 can{15};
    ActuationManager manager{&Wire, &can};
    return 0;
}

