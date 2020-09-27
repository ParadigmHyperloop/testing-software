#include "DPS310.h"

DPS310::DPS310()
    : m_address(s_defaultAddress)
{}

DPS310::DPS310(const uint8_t address)
    : m_address(address)
{}


/**
 * Returns a byte indicating transmission status:
 *      0: Success
 *      1: Data too long to fit in transmission buffer
 *      2: Received NACK on transmit of address
 *      3: Received NACK on transmit of data
 *      4: Other error
 */
byte_t DPS310::writeRegister(const Register reg, const uint8_t value)
{
    Wire.beginTransmission(m_address);
    Wire.write(value);
    byte_t result = Wire.endTransmission();
    
    return result;
}

int32_t DPS310::readCalibrationCoefficient(const Coefficient_Reg reg)
{
    uint8_t high_byte = 0, middle_byte = 0, low_byte = 0;
    int32_t result = 0;
    switch (reg)
    {
        case C0:
        {
            Wire.beginTransmission(m_address);
            Wire.write(C0);
            Wire.requestFrom(m_address, 2);
            high_byte = Wire.read();
            low_byte = Wire.read();
            result = (high_byte << 4) | ((low_byte & 0xf0) >> 4);
            break;
        }
        case C1:
        {
            Wire.beginTransmission(m_address);
            Wire.write(C1);
            Wire.requestFrom(m_address, 2);
            high_byte = Wire.read();
            low_byte = Wire.read();
            result = ((high_byte & 0x0f) << 8) | low_byte;
            break;
        }
        case C00:
        {
            Wire.beginTransmission(m_address);
            Wire.write(C00);
            Wire.requestFrom(m_address, 3);
            high_byte = Wire.read();
            middle_byte = Wire.read();
            low_byte = Wire.read();
            result = (high_byte << 12) | (middle_byte << 4) | ((low_byte & 0xf0) >> 4);
        }
        case C10:
        {
            Wire.beginTransmission(m_address);
            Wire.write(C10);
            Wire.requestFrom(m_address, 3);
            high_byte = Wire.read();
            middle_byte = Wire.read();
            low_byte = Wire.read();
            result = ((high_byte & 0x0f) << 16) | (middle_byte << 8) | low_byte;
        }
        case C11:
        {
            Wire.beginTransmission(m_address);
            Wire.write(C11);
            Wire.requestFrom(m_address, 2);
            high_byte = Wire.read();
            low_byte = Wire.read();
            result = (high_byte << 8) | low_byte;
        }
        case C20:
        {
            Wire.beginTransmission(m_address);
            Wire.write(C20);
            Wire.requestFrom(m_address, 2);
            high_byte = Wire.read();
            low_byte = Wire.read();
            result = (high_byte << 8) | low_byte;
        }
        case C21:
        {
            Wire.beginTransmission(m_address);
            Wire.write(C21);
            Wire.requestFrom(m_address, 2);
            high_byte = Wire.read();
            low_byte = Wire.read();
            result = (high_byte << 8) | low_byte;
        }
        case C30:
        {
            Wire.beginTransmission(m_address);
            Wire.write(C30);
            Wire.requestFrom(m_address, 2);
            high_byte = Wire.read();
            low_byte = Wire.read();
            result = (high_byte << 8) | low_byte;
        }
    }
    
    return result;
}

byte_t DPS310::configureTemp(byte_t tempRate, byte_t tempPrecision)
{
    return writeRegister(TMP_CFG, (tempRate & 0xf0) | (tempPrecision & 0x0f));
}

byte_t DPS310::configurePressure(byte_t pressureRate, byte_t pressurePrecision)
{
    return writeRegister(PRS_CFG, (pressureRate & 0xf0) | (pressurePrecision & 0x0f));
}