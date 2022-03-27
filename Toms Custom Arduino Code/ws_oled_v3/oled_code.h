#include <Arduino.h>
#include <SPI.h>
#include <stdint.h>


// DIN and CLK must be connected to MOSI and SCK pins on the arduino respectively
// This should be pins 11 and 13 respectively on an Uno or Nano 33 IOT for example

class WaveShareOled {
    private:
        char CS;
        char DC;
        char RST;

        unsigned int displayWidth;
        unsigned int displayHeight;

        void oledWriteReg(uint8_t reg);
        void oledWriteData(uint8_t data);

    public:
        // Constructor
        WaveShareOled();
        int begin(char CS, char DC, char RST, uint16_t displayWidth, uint16_t displayHeight);
};