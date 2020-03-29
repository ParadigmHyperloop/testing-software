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
    SPIClass spi;
    SPISettings spiSettings = SPISettings(20000000, MSBFIRST, SPI_MODE0);
    uint8_t SS_PIN;
    uint8_t POWER_SEQ_PIN;
    bool HAS_SEQ_PIN = false;
    // 16-bit data words for SPI
    const uint16_t SET_CHANNEL_REG = 0x8000;
    const uint16_t CONFIG_PROGRAM_REG = 0x2840;
    const uint16_t MANUAL_READ = 0x1000;
    const uint16_t AUTO_READ_RESET = 0x2C40;
    const uint16_t AUTO_READ_NEXT = 0x2000;
    const uint8_t WAKEUP = 0x02;
    const uint8_t POWERDOWN = 0x04;
    const uint8_t RESET = 0x06;

    uint16_t uAdcData[16]{};      //array of the latest data; 0 for channels not being used
    uint16_t uActiveChannels = 0; // each bit represents a channel; 1=used, 0=unused
    uint16_t uNumChannels = 0;    // number of channels being used;

    uint16_t transfer(uint16_t uData);
};

#endif