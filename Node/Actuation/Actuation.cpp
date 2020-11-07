#include "Actuation.h"

ActuationManager::ActuationManager(TwoWire* pI2C, const uint8_t u8Cs)
    : m_pI2C(pI2C), m_can(u8Cs), m_motorShield()
{}

bool ActuationManager::receiveCommand()
{
    can_frame frame = {0};
    MCP2515::ERROR response = m_can.readMessage(&frame);
    if (response != MCP2515::ERROR_OK)
    {
        // TODO handle error here
        return false;
    }
    switch (frame.can_id)
    {
        case (eInitCommand):
        {
            uint16_t u16Data = (frame.data[0] << 8) | frame.data[1];
            uint8_t u8Address = frame.data[2];
            InitStepper(u16Data, u8Address);
            break;
        }
        case (eSpeedCommand):
        {
            uint16_t u16Data = (frame.data[0] << 8) | frame.data[1];
            uint8_t u8Address = frame.data[2];
            setStepperSpeed(u16Data, u8Address);
            break;
        }
        case (eStepCommand):
        {
            break;
        }
    }

    return true;
}

void ActuationManager::InitStepper(uint16_t u16Step, uint8_t u8Address)
{
    if (u8Address != 1 || u8Address != 2)
    {
        // TODO error handling
        return;
    }
    if (m_apSteppers[u8Address - 1] == nullptr)
    {
        m_apSteppers[u8Address - 1] = m_motorShield.getStepper(u16Step, u8Address);
    }
    sendInitStepperResponse(u16Step, u8Address);
}

void ActuationManager::sendInitStepperResponse(uint16_t u16Step, uint8_t u8Address)
{
    uint8_t au8Data[] = { (uint8_t)((u16Step & 0xFF00) >> 8), (uint8_t)(u16Step & 0x00FF), u8Address };
    can_frame frame = { eInitResponse, 8, au8Data };

    MCP2515::ERROR status = m_can.sendMessage(&frame);
    if (status != MCP2515::ERROR_OK)
    {
        // TODO error handling
    }
}

void ActuationManager::setStepperSpeed(uint16_t u16Speed, uint8_t u8Address)
{
    if (m_apSteppers[u8Address - 1] == nullptr)
    {
        // TODO error handling
        return;
    }
    m_apSteppers[u8Address - 1]->setSpeed(u16Speed);

    sendStepperSpeedResponse(u16Speed, u8Address);
}

void ActuationManager::sendStepperSpeedResponse(uint16_t u16Speed, uint8_t u8Address)
{
    uint8_t au8Data[] = { (uint8_t)((u16Speed & 0xFF00) >> 8), (uint8_t)(u16Speed & 0x00FF), u8Address };
    can_frame frame = { eSpeedResponse, 8, au8Data };

    MCP2515::ERROR status = m_can.sendMessage(&frame);
    if (status != MCP2515::ERROR_OK)
    {
        // TODO error handling
    }
}

int main(void)
{
    ActuationManager manager{&Wire, 15};
    return 0;
}

