#include "adc_ADS114S0.h"

ADS114S0::ADS114S0(const uint8_t CS)
    : m_CS(CS)
{
    SPI.begin();

    pinMode(m_CS, OUTPUT);
    endSPI();
}

void ADS114S0::beginSPI()
{
    SPI.beginTransaction(SPISettings(SPI_CLOCK, MSBFIRST, SPI_MODE1));
    digitalWrite(m_CS, LOW);
}

void ADS114S0::endSPI()
{
    digitalWrite(m_CS, HIGH);
    SPI.endTransaction();
}

void ADS114S0::reset()
{
    beginSPI();
    SPI.transfer(RESET);
    endSPI();

    delay(10);

    writeRegisters(STATUS, DEFAULTS, 16);
}

void ADS114S0::writeRegister(const Register reg, const uint8_t value)
{
    beginSPI();
    SPI.transfer16(WREG | ((reg<<8) & 0xff00));
    SPI.transfer(value);
    endSPI();
}

void ADS114S0::writeRegisters(const Register reg, const uint8_t values[], const uint8_t num)
{
    beginSPI();
    SPI.transfer16(WREG | ((reg<<8) & 0xff00) | ((num - 1) & (0x00ff)));
    for (uint8_t i = 0; i < num; i++)
    {
        SPI.transfer(values[i]);
    }
    endSPI();
}

uint8_t ADS114S0::readRegister(const Register reg)
{
    beginSPI();
    SPI.transfer16(RREG | ((reg<<8) & 0xff00));
    uint8_t value = SPI.transfer(0x00);
    endSPI();

    return value;
}

void ADS114S0::readRegisters(const Register reg, uint8_t values[], const uint8_t num)
{
    beginSPI();
    SPI.transfer16(WREG | ((reg<<8) & 0xff00) | ((num - 1) & (0x00ff)));
    for (uint8_t i = 0; i < num; i++)
    {
        values[i] = SPI.transfer(0x00);
    }
    endSPI();
}

void ADS114S0::setMux(const InputMux mux)
{
    writeRegister(INPMUX, mux);
}

void ADS114S0::setPGAGain(const PGAGain gain)
{
    writeRegister(PGA, gain);
}

void ADS114S0::setMode(const DataRate rate, const ClockSource clock, const ConversionMode mode)
{
    writeRegister(DATARATE, rate | clock | mode);
}

void ADS114S0::setConversionMode(const ConversionMode mode)
{
    uint8_t currentSettings = readRegister(DATARATE);
    writeRegister(DATARATE, currentSettings | mode);
}

void ADS114S0::startConversion()
{
    beginSPI();
    SPI.transfer(START);
    endSPI();
}

void ADS114S0::stopConversion()
{
    beginSPI();
    SPI.transfer(STOP);
    endSPI();
}

uint16_t ADS114S0::readData()
{
    beginSPI();
    SPI.transfer(RDATA);
    uint16_t data = SPI.transfer16(0x0000);
    endSPI();

    return data;
}
