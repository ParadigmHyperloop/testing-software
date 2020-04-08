#include "adc_ADS114S0.h"

ADS114S0::ADS114S0(SPIClass spi, uint8_t SS_PIN) : spi(spi), SS_PIN(SS_PIN)
{
}

void ADS114S0::init()
{
    pinMode(SS_PIN, OUTPUT);
    spi.begin();
    spi.beginTransaction(spiSettings);
    digitalWrite(SS_PIN, LOW);
    uint8_t reset = spi.transfer(RESET);
    delay(4096 * (1 / 20000000));
    uint16_t resetStatus = spi.transfer16(0x3101);
    uint8_t writeReg = spi.transfer(0x00);
    digitalWrite(SS_PIN, HIGH);
    spi.endTransaction();
}

void ADS114S0::writeRegister(uint8_t reg, uint8_t value)
{
    uint16_t command = ((0x40 + reg) << 8) + 0x01;
    spi.beginTransaction(spiSettings);
    digitalWrite(SS_PIN, LOW);
    spi.transfer16(command);
    spi.transfer(value);
    digitalWrite(SS_PIN, HIGH);
    spi.endTransaction();
}

uint8_t ADS114S0::readRegister(uint8_t reg)
{
    uint16_t command = ((0x20 + reg) << 8) + 0x01;
    spi.beginTransaction(spiSettings);
    digitalWrite(SS_PIN, LOW);
    spi.transfer16(command);
    uint8_t data = spi.transfer(0x00);
    digitalWrite(SS_PIN, HIGH);
    spi.endTransaction();
    return data;
}

uint16_t ADS114S0::readData()
{
    spi.beginTransaction(spiSettings);
    digitalWrite(SS_PIN, LOW);
    spi.transfer(RDATA);
    uint16_t data = spi.transfer16(0x0000);
    digitalWrite(SS_PIN, HIGH);
    spi.endTransaction();
    return data;
}

void ADS114S0::setMux(InputMux mux)
{
    uint16_t writeCommand = 0x4201;
    spi.beginTransaction(spiSettings);
    digitalWrite(SS_PIN, LOW);
    spi.transfer16(writeCommand);
    spi.transfer(mux);
    digitalWrite(SS_PIN, HIGH);
    spi.endTransaction();
}

void ADS114S0::setPGAGain(PGAGain gain)
{
    uint16_t writeCommand = 0x4301;
    spi.beginTransaction(spiSettings);
    digitalWrite(SS_PIN, LOW);
    spi.transfer16(writeCommand);
    spi.transfer(gain);
    digitalWrite(SS_PIN, HIGH);
    spi.endTransaction();
}

void ADS114S0::setDataRate(DataRate rate)
{
    uint16_t writeCommand = 0x4401;
    spi.beginTransaction(spiSettings);
    digitalWrite(SS_PIN, LOW);
    spi.transfer16(writeCommand);
    spi.transfer(rate);
    digitalWrite(SS_PIN, HIGH);
    spi.endTransaction();
}

void ADS114S0::startConversion()
{
    spi.beginTransaction(spiSettings);
    digitalWrite(SS_PIN, LOW);
    spi.transfer(START);
    digitalWrite(SS_PIN, HIGH);
    spi.endTransaction();
}

void ADS114S0::stopConversion()
{
    spi.beginTransaction(spiSettings);
    digitalWrite(SS_PIN, LOW);
    spi.transfer(STOP);
    digitalWrite(SS_PIN, HIGH);
    spi.endTransaction();
}