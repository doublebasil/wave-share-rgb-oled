#include "image.h"

void setup() {
    Serial.begin(9600);

    for (int i = 0; i <= 151; i++) {
        Serial.println(*dataPointers[i]);
        Serial.println(array2Idk[12]);
    }
}

void loop() {

}