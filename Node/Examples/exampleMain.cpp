#include <Arduino.h>

#include "mcp2515.h"

void setup()
{
    pinMode(PIN_SPI_SS, OUTPUT);

    MCP2515 mcp2515{PIN_SPI_SS};
}

void loop()
{
    digitalWrite(LED_BUILTIN, HIGH);
    delay(1000);
    digitalWrite(LED_BUILTIN, LOW);
    delay(1000);
}
