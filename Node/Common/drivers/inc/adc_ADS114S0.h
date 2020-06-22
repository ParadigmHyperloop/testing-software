#ifndef ADC_ADS114S0_H
#define ADC_ADS114S0_H

#include <SPI.h>

enum class InputMux: uint8_t
{
    MUX_SINGLE_0    = 0x0C, // Single-ended AIN0
    MUX_SINGLE_1    = 0x1C, // Single-ended AIN1
    MUX_SINGLE_2    = 0x2C, // Single-ended AIN2
    MUX_SINGLE_3    = 0x3C, // Single-ended AIN3
    MUX_SINGLE_4    = 0x4C, // Single-ended AIN4
    MUX_SINGLE_5    = 0x5C, // Single-ended AIN5
    MUX_SINGLE_6    = 0x6C, // Single-ended AIN6
    MUX_SINGLE_7    = 0x7C, // Single-ended AIN7
    MUX_SINGLE_8    = 0x8C, // Single-ended AIN8
    MUX_SINGLE_9    = 0x9C, // Single-ended AIN9
    MUX_SINGLE_10   = 0xAC, // Single-ended AIN10
    MUX_SINGLE_11   = 0xBC  // Single-ended AIN11
};

enum class PGAGain: uint8_t
{
    GAIN_DISABLE    = 0x00, // Default
    GAIN_2          = 0x09,
    GAIN_4          = 0x0A,
    GAIN_8          = 0x0B,
    GAIN_16         = 0x0C,
    GAIN_32         = 0x0D,
    GAIN_64         = 0x0E,
    GAIN_128        = 0x0F
};

enum class DataRate: uint8_t
{
    SPS_2_5     = 0x10, // 2.5 Samples Per Second
    SPS_5       = 0x11, // 5 Samples Per Second
    SPS_10      = 0x12, // 10 Samples Per Second
    SPS_16_6    = 0x13, // 16.6 Samples Per Second
    SPS_20      = 0x14, // 20 Samples Per Second (default)
    SPS_50      = 0x15, // 50 Samples Per Second
    SPS_60      = 0x16, // 60 Samples Per Second
    SPS_100     = 0x17, // 100 Samples Per Second
    SPS_200     = 0x18, // 200 Samples Per Second
    SPS_400     = 0x19, // 400 Samples Per Second
    SPS_800     = 0x1A, // 800 Samples Per Second
    SPS_1000    = 0x1B, // 1000 Samples Per Second
    SPS_2000    = 0x1C, // 2000 Samples Per Second
    SPS_4000    = 0x1D  // 4000 Samples Per Second
};

enum class Command: uint8_t
{
    WAKEUP      = 0x02,
    POWERDOWN   = 0x04,
    RESET       = 0x06,
    START       = 0x08,
    STOP        = 0x0A,
    SYOCAL      = 0x16, // System offset calibration
    SYGCAL      = 0x17, // System gain calibration
    SFOCAL      = 0x19, // Self offset calibration
    RDATA       = 0x12
};

class ADS114S0
{
public:
    ADS114S0(uint8_t CS);
    void init();
    void writeRegister(uint8_t, uint8_t);
    uint8_t readRegister(uint8_t);
    uint16_t readData();
    void setMux(InputMux);
    void setPGAGain(PGAGain);
    void setDataRate(DataRate);
    void startConversion();
    void stopConversion();

private:
    SPIClass spi;
    SPISettings spiSettings = SPISettings(20000000, MSBFIRST, SPI_MODE1);
    uint8_t CS;
    uint8_t DRDY_PIN;
};

#endif
