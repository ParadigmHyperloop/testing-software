#include "adc_ADS114S0.h"

ADS114S0::ADS114S0(SPIClass spi, uint8_t SS_PIN, uint8_t POWER_SEQ_PIN) : spi(spi), SS_PIN(SS_PIN), POWER_SEQ_PIN(POWER_SEQ_PIN)
{
    HAS_SEQ_PIN = true;
}

ADS114S0::ADS114S0(SPIClass spi, uint8_t SS_PIN) : spi(spi), SS_PIN(SS_PIN)
{
}

void ADS114S0::init()
{
    spi.begin();
    pinMode(SS_PIN, OUTPUT);
    digitalWrite(SS_PIN, HIGH);
}