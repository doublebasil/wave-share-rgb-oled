/*
Note:   to compile you need to link the main and
        the header file:
        g++ main2.cpp exec2.cpp
*/

#include "ws_image.hpp"

#define CS_PIN 10
#define DC_PIN 7
#define RST_PIN 8

#define DISPLAY_WIDTH 128
#define DISPLAY_HEIGHT 128

WSImageSender obj;

void setup() {
    Serial.begin(9600);
    
    obj.begin(CS_PIN, DC_PIN, RST_PIN, DISPLAY_WIDTH, DISPLAY_HEIGHT);
    obj.sendImage();
}

void loop() {

}
