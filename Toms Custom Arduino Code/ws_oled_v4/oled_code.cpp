#include "oled_code.h"
// --- Private class methods

void WaveShareOled::oledWriteReg(uint8_t reg) {
    digitalWrite(DC, 0);
    digitalWrite(CS, 0);
    SPI.transfer(reg);
    digitalWrite(CS, 1);
}

void WaveShareOled::oledWriteData(uint8_t data) {
    digitalWrite(DC, 1);
    digitalWrite(CS, 0);
    SPI.transfer(data);
    digitalWrite(CS, 1);
}

// --- Public class methods

WaveShareOled::WaveShareOled() {}

int WaveShareOled::begin(char CS, char DC, char RST, uint16_t displayWidth, uint16_t displayHeight) {
    // Init Arduino pins
    pinMode(CS, OUTPUT);
    pinMode(RST, OUTPUT);
    pinMode(DC, OUTPUT);
    // pinMode(DIN, OUTPUT); // There's actually no mention of these in pinMode
    // pinMode(CLK, OUTPUT); // Perhaps because they're the SPI pins? (yes they are)

    // SPI setup
    SPI.setDataMode(SPI_MODE3);
    SPI.setBitOrder(MSBFIRST);
    SPI.setClockDivider(SPI_CLOCK_DIV2);
    SPI.begin();

    // In manufacturer code, serial was started here

    // Set object variable values to constructor args
    this->CS = CS;
    this->DC = DC;
    this->RST = RST;

    // // Reset the display by setting the reset pin low
    // // NTS: Fiddle with the delay times or maybe find a datasheet?
    digitalWrite(RST, 1);
    delay(100);
    digitalWrite(RST, 0);
    delay(100);
    digitalWrite(RST, 1);
    delay(100);

    // // Now for some inexplicable magic from the manufacturer. Comments here are from the manufacturer code
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
    // // // End of inexplicable code

    // // // Turn on the display
    oledWriteReg(0xAF);

    delay(500);

    // // The screen is then cleared using this interesting code
    oledWriteReg(0x15);
    oledWriteData(0);
    oledWriteData(127);
    oledWriteReg(0x75);
    oledWriteData(0);
    oledWriteData(127);
    // // fill!
    oledWriteReg(0x5C);

    for (uint32_t i = 0; i < displayWidth * displayHeight * 2; i++) {
        oledWriteData(0x00);
    }


    // 0 = black
    // 128 = red
    // 255 = white

    // for (uint32_t j = 0; j < 256; j += 1) {
    //     for (uint32_t i = 0; i < displayWidth * displayHeight * 2; i++) {
    //         oledWriteData(j);
    //         // delay(10);
    //     }
    // }

    for (uint32_t j = 0; j < displayHeight * 2; j += 2) {
        for (uint32_t i = 0; i < displayWidth * 2; i++) {
            oledWriteData(j);
            // delay(10);
        }
    }
    


    // Serial.println("Done");

}

