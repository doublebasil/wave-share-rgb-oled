#include "oled_code.h"

// --- Private class methods

#ifdef DEBUG_PIN
void WaveShareOled::DEBUG_ON() {
    digitalWrite(DEBUG_PIN, HIGH);
}

void WaveShareOled::DEBUG_OFF() {
    digitalWrite(DEBUG_PIN, LOW);
}
#endif

void WaveShareOled::oledWriteReg(DTYPE reg) {
    digitalWrite(DC, 0);
    digitalWrite(CS, 0);
    SPI.transfer(reg);
    digitalWrite(CS, 1);
}

void WaveShareOled::oledWriteData(DTYPE dataOut) {
    digitalWrite(DC, 1);
    digitalWrite(CS, 0);
    SPI.transfer(dataOut);
    digitalWrite(CS, 1);
}

// --- Public class methods

WaveShareOled::WaveShareOled() {}

void WaveShareOled::clear(void) {
    // This code cannot be used for setting the display to any other color

    oledWriteReg(0x15);
    oledWriteData(0);
    oledWriteData(127);
    oledWriteReg(0x75);
    oledWriteData(0);
    oledWriteData(127);

    oledWriteReg(0x5C);

    for (uint16_t i = 0; i < displayWidth * displayHeight * 2; i++) {
        oledWriteData(0x0000);
    }
    
}

int WaveShareOled::begin(char CS, char DC, char RST, uint16_t displayWidth, uint16_t displayHeight) {
    // Init Arduino pins
    pinMode(CS, OUTPUT);
    pinMode(RST, OUTPUT);
    pinMode(DC, OUTPUT);
    // DIN and CLK pins don't need to be set to output as they are the SPI pins

    // Debug LED if required
    #ifdef DEBUG_PIN
    pinMode(DEBUG_PIN, OUTPUT);
    #endif

    // SPI setup
    SPI.setDataMode(SPI_MODE3);
    SPI.setBitOrder(MSBFIRST);
    SPI.setClockDivider(SPI_CLOCK_DIV2);
    SPI.begin();

    // Set object variable values to constructor args
    this->CS = CS;
    this->DC = DC;
    this->RST = RST;

    this->displayWidth = displayWidth;
    this->displayHeight = displayHeight;

    // Reset the display by setting the reset pin low
    // NTS: Fiddle with the delay times or maybe find a datasheet?
    digitalWrite(RST, 1);
    delay(100);
    digitalWrite(RST, 0);
    delay(100);
    digitalWrite(RST, 1);
    delay(100);

    // Now for some inexplicable magic from the manufacturer. Comments here are from the manufacturer code
    oledWriteReg(0xFD);  // Command lock
    oledWriteData(0x12);
    oledWriteReg(0xFD);  // Command lock
    oledWriteData(0xB1);

    oledWriteReg(0xAE);  // Display off
    oledWriteReg(0xA4);  // Normal Display mode

    oledWriteReg(0x15);  // Set column address
    oledWriteData(0x00); // Column address start 00
    oledWriteData(0x7F); // Column address end 127
    oledWriteReg(0x75);  // Set row address
    oledWriteData(0x00); // Row address start 00
    oledWriteData(0x7F); // Row address end 127    

    oledWriteReg(0xB3);
    oledWriteData(0xF1);

    oledWriteReg(0xCA);  
    oledWriteData(0x7F);

    oledWriteReg(0xA0);  // Set re-map & data format
    oledWriteData(0x74); // Horizontal address increment

    oledWriteReg(0xA1);  // Set display start line
    oledWriteData(0x00); // Start 00 line

    oledWriteReg(0xA2);  // Set display offset
    oledWriteData(0x00);

    oledWriteReg(0xAB);  
    oledWriteReg(0x01);  

    oledWriteReg(0xB4);  
    oledWriteData(0xA0);   
    oledWriteData(0xB5);  
    oledWriteData(0x55);    

    oledWriteReg(0xC1);  
    oledWriteData(0xC8); 
    oledWriteData(0x80);
    oledWriteData(0xC0);

    oledWriteReg(0xC7);  
    oledWriteData(0x0F);

    oledWriteReg(0xB1);  
    oledWriteData(0x32);

    oledWriteReg(0xB2);  
    oledWriteData(0xA4);
    oledWriteData(0x00);
    oledWriteData(0x00);

    oledWriteReg(0xBB);  
    oledWriteData(0x17);

    oledWriteReg(0xB6);
    oledWriteData(0x01);

    oledWriteReg(0xBE);
    oledWriteData(0x05);

    oledWriteReg(0xA6);

    delay(200);
    // End of inexplicable code

    // Turn on the display
    oledWriteReg(0xAF);

    delay(500);

    clear();

    return 0;

}

void WaveShareOled::fill(DTYPE color) {
    oledWriteReg(0x15);
    oledWriteData(0);
    oledWriteData(127);
    oledWriteReg(0x75);
    oledWriteData(0);
    oledWriteData(127);

    oledWriteReg(0x5C);

    for (uint32_t i = 0; i < displayWidth * displayHeight * 2; i++) {
        oledWriteData(color);
    }
}

void WaveShareOled::setPixel(uint16_t x, uint16_t y, DTYPE color) {
    oledWriteReg(0x15);
    oledWriteData(x);
    oledWriteData(x);
    oledWriteReg(0x75);
    oledWriteData(y);
    oledWriteData(y);
    // fill!
    oledWriteReg(0x5C);   
    
    oledWriteData(color >> 8); // Don't ask I don't know
    oledWriteData(color);
}

