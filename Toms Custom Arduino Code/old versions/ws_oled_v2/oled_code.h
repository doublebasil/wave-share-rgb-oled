#include <Arduino.h>
#include <SPI.h>
#include <stdint.h>

static char CS;
static char DC;
static char RST;
static uint16_t displayWidth;
static uint16_t displayHeight;

// Behind-the-scenes functions
void oledWriteReg(uint8_t reg);
void oledWriteData(uint8_t data);

// User functions
svoid oledInit(char CS, char DC, char RST, uint16_t displayWidth, uint16_t displayHeight);