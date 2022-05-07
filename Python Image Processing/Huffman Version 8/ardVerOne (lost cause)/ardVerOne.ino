#include <Arduino.h>
#include "exec.h"

#include "oled_code.h"

// Pins for oled screen
#define CS_PIN 10
#define DC_PIN 7
#define RST_PIN 8

WaveShareOled oled = WaveShareOled();

void setup() {
    Serial.begin(9600);
    Serial.println("Made it to setup :)");

    oled.begin(CS_PIN, DC_PIN, RST_PIN, DISPLAY_WIDTH, DISPLAY_HEIGHT);

    Serial.println("oled.begin finished");

    sendImage(oled);

}

void loop() {

}
