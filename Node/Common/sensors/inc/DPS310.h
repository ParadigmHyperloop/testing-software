#ifndef DPS310_H
#define DPS310_H
#include "Arduino.h"
#include "Wire.h"

using byte_t = uint8_t;

enum Register : uint8_t
{
    PSR_B2      = 0x00,
    PSR_B1      = 0x01,
    PSR_B0      = 0x02,
    TMP_B2      = 0x03,
    TMP_B1      = 0x04,
    TMP_B0      = 0x05,
    PRS_CFG     = 0x06,
    TMP_CFG     = 0x07,
    MEAS_CFG    = 0x08,
    CFG_REG     = 0x09,
    INT_STS     = 0x0A,
    FIFO_STS    = 0x0B,
    RESET       = 0x0C
};

enum Coefficient_Reg : uint8_t
{
    C0  = 0x10,
    C1  = 0x11,
    C00 = 0x13,
    C10 = 0x15,
    C01 = 0x18,
    C11 = 0x1A,
    C20 = 0x1C,
    C21 = 0x1E,
    C30 = 0x20
};

enum Configuration_Reg : uint8_t
{
    
};

// Pressure sensors use the high speed clock by default
constexpr unsigned HIGH_SPEED_MODE = 3400000;

/**********************************************\
 *  I2C Interface for DPS310 Pressure Sensor  *
\**********************************************/
class DPS310
{
public:
    static const unsigned s_defaultAddress = 77;

    DPS310();
    DPS310(const uint8_t);
    byte_t writeRegister(const Register, const uint8_t);
    int32_t readCalibrationCoefficient(const Coefficient_Reg);
    byte_t configureTemp(byte_t, byte_t);
    byte_t configurePressure(byte_t, byte_t);

private:
    uint8_t m_address;
};
#endif