#include "oled_code.h"

// Pins for oled screen
#define CS_PIN 10
#define DC_PIN 7
#define RST_PIN 8
#define DIN_PIN 11
#define CLK_PIN 13

#define DISPLAY_WIDTH 128
#define DISPLAY_HEIGHT 128

WaveShareOled oled = WaveShareOled();

void setup() {
    Serial.begin(9600);
    Serial.println("Made it to setup :)");

    long a = millis();

    oled.begin(CS_PIN, DC_PIN, RST_PIN, DISPLAY_WIDTH, DISPLAY_HEIGHT);

    long b = millis() - a;

    Serial.print("Made it past init in ");
    Serial.print(b);
    Serial.println("ms!");

    // DTYPE myColor;
    // delay(2000);
    // Serial.println(" --- ");
    // Serial.println("0xF800 = RED");
    // myColor = 0xF800;
    // oled.fill(myColor);
    // delay(2000);
    // Serial.println("0x07E0 = GREEN");
    // myColor = 0x07E0;
    // oled.fill(myColor);
    // delay(2000);
    // Serial.println("0x001F = BLUE");
    // myColor = 0x001F;
    // oled.fill(myColor);
    // delay(2000);
    // Serial.println("0xFFE0 = GRED");
    // myColor = 0xFFE0;
    // oled.fill(myColor);
    // delay(2000);

    for (int x = 10; x < 20; x++) {
        for (int y = 10; y < 20; y++) {
            oled.setPixel(x, y, 0xFFE0);
        }
    }
    oled.setPixel(0, 0, 0xF2);

    // oled.clear();

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
