// #define DEBUG_PIN 2 // Attach an LED to this pin for debugging

// NTS: Change the debug led stuff to be functions, and test if debug works
// withing clear() (I suspect it doesn't)

// DIN and CLK must be connected to MOSI and SCK pins on the arduino respectively
// This should be pins 11 and 13 respectively on an Uno or Nano 33 IOT for example
#include <Arduino.h>
#include <SPI.h>
#include <stdint.h>

// WaveShareOled
class WSOled 
{
    // Must not be private so that a derived class is able to use
    protected:
        char CS;
        char DC;
        char RST;

        unsigned int displayWidth;
        unsigned int displayHeight;

        #ifdef DEBUG_PIN
        void DEBUG_ON();
        void DEBUG_OFF();
        #endif

        void oledWriteReg(uint8_t reg);
        void oledWriteData(uint8_t dataOut);

    public:
        WSOled();
        void clear(void);
        int begin(char CS, char DC, char RST, uint16_t displayWidth, uint16_t displayHeight);
        // void fill(DTYPE color);
        void setPixel(uint16_t x, uint16_t y, uint16_t color);
};
