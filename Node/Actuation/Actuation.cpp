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
            InitializeStepper(u16Data, u8Address);
            break;
        }
        case (eSpeedCommand):
        {
            break;
        }
        case (eStepCommand):
        {
            break;
        }
    }

    return true;
}

void AcutationManager::InitializeStepper(uint16_t u16Step, uint8_t u8Address)
{

}

int main(void)
{
    ActuationManager manager{&Wire, 15};
    return 0;
}

