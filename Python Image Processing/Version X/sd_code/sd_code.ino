#include <SPI.h>
#include <SD.h>
#include <stdint.h>

#include "oled_code.hpp"

/*
 * MOSI - 11
 * MISO - 12
 * CLK
 * 
 */

#define CS_PIN 10
#define DC_PIN 7
#define RST_PIN 8
#define DISPLAY_WIDTH 128
#define DISPLAY_HEIGHT 128
WaveShareOled oled = WaveShareOled();

File myFile;

// IMPORTANT NOTE
// Seems there is a rather short file name length limit!
// Use filenames such as "im.txt" rather than "imagedata123.txt"

void numericReadTest() {
  Serial.begin(115200);
  while(!Serial) {}

  Serial.print("Initialising oled... ");
  oled.begin(CS_PIN, DC_PIN, RST_PIN, DISPLAY_WIDTH, DISPLAY_HEIGHT);
  Serial.println(" done.");

  Serial.print("Loading SD card... ");

  if (!SD.begin(4)) {
    Serial.println(" Failed :(");
    while (1) {
      delay(1000);
    }
  }
  Serial.println(" Success!");

  unsigned long dataIn;

  myFile = SD.open("IM.TXT");
  if (myFile) {

    // Get the width of the display
    uint32_t displayWidth = 0;
    for (int i = 0; i < 3; i++) {
      if (! myFile.available()) {
        Serial.println("File ended unexpectedly");
        while (1) {delay(1000);}
      }
      displayWidth += ((uint32_t) (myFile.read() - 32) << ((2 - i) * 6));
    }
    Serial.print("Display width is ");
    Serial.println(displayWidth);
    
    // Get the height of the display
    uint32_t displayHeight = 0;
    for (int i = 0; i < 3; i++) {
      if (! myFile.available()) {
        Serial.println("File ended unexpectedly");
        while (1) {delay(1000);}
      }
      displayHeight += ((uint32_t) (myFile.read() - 32) << ((2 - i) * 6));
    }
    Serial.print("Display height is ");
    Serial.println(displayHeight);

    // Get all the pixels from the file
    uint32_t x = 0;
    uint32_t y = 0;
    uint64_t dataBuffer;
    while (1) {
      dataBuffer = 0;
      // Read 8 characters, this is equal to 3 words (3 pixels)
      for (int i = 0; i < 8; i++) {
        if (myFile.available()) {
          dataBuffer += ((uint64_t) (myFile.read() - 32) << ((7 - i) * 6));
        }
      }

//      Serial.println((uint32_t) dataBuffer >> 32);
//      Serial.println((uint32_t) dataBuffer);
//      while (1) {delay(1000);}
      
      // Now convert dataBuffer into 3 words and output to screen
      for (int i = 0; i < 3; i++) {
        uint16_t out = (((uint64_t) dataBuffer >> ((2 - i) * 16)) & 0b1111111111111111);

//        if (y == 127) {
//          Serial.print("(");
//          Serial.print(x);
//          Serial.print(", ");
//          Serial.print(y);
//          Serial.print(") -> ");
//          Serial.println(out);
//        }

        oled.setPixel(x, y, out);

        x++;
        if (x == displayWidth) {
          y++;
          x = 0;
          if (y == displayHeight) {
            break;
          }
        }
      }
      if (y == displayHeight) {
        break;
      }
    }

    myFile.close();
  }
  else {
    Serial.println("Error opening file");
  }
}


void setup() {
  numericReadTest();
}

void loop() {
  
}
