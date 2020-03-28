#ifndef ADC_ADS114S0_H
#define ADC_ADS114S0_H

#include <SPI.h>

class ADS114S0
{
public:
    ADS114S0(SPIClass spi, uint8_t SS_PIN, uint8_t POWER_SEQ_PIN);
    ADS114S0(SPIClass spi, uint8_t SS_PIN);
    void init();
    uint16_t readSingleChannel(uint8_t);
    void readActiveChannels();
    void enableChannel(uint8_t);
    void disableChannel(uint8_t);
    uint16_t *getuAdcData() { return uAdcData; };

private:
};

#endif