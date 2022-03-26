#include "oled_code.h"

// Pins for oled screen
#define CS_PIN 10
#define DC_PIN 7
#define RST_PIN 8
#define DIN_PIN 11
#define CLK_PIN 13

#define DISPLAY_WIDTH 128
#define DISPLAY_HEIGHT 128

WaveShareOled oled = WaveShareOled(CS_PIN, DC_PIN, RST_PIN, DISPLAY_WIDTH, DISPLAY_HEIGHT);

void setup() {
    // Serial.begin(9600);
    // Serial.println("Back to ino");

    // pinMode(LED_BUILTIN, OUTPUT);
    // digitalWrite(LED_BUILTIN, HIGH);
    
    // if (!Serial) {
    //     Serial.begin(9600);
    //     delay(100);
    //     Serial.println("Started Serial in main");
    // }


    // int prev = (int) Serial; // serial only tells you if the usb is ready
    // Serial.begin(9600);
    // Serial.println("Test");
    // Serial.print("Now we have ");
    // Serial.println(Serial);
    // Serial.print("Before we had ");
    // Serial.println(prev);
}

void loop() {
  
}
