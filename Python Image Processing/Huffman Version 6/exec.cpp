#include <iostream>
#include <stdio.h>
#include <stdint.h>
#include "image.h"

using namespace std;

void send(uint16_t data) {
    cout << data << endl;
}

void setup() {
    // cout << hex << endl;
}

// #define BYTE_TO_BINARY_PATTERN "%c%c%c%c%c%c%c%c"
// #define BYTE_TO_BINARY(byte)  \
//     (byte & 0x80 ? '1' : '0'), \
//     (byte & 0x40 ? '1' : '0'), \
//     (byte & 0x20 ? '1' : '0'), \
//     (byte & 0x10 ? '1' : '0'), \
//     (byte & 0x08 ? '1' : '0'), \
//     (byte & 0x04 ? '1' : '0'), \
//     (byte & 0x02 ? '1' : '0'), \
//     (byte & 0x01 ? '1' : '0')

void printBin(uint64_t num, uint8_t bits) {
    uint64_t indexor = 1 << (bits - 1);
    // Counter to decide where to put spaces
    uint8_t spaceCounter = bits % 4;
    if (spaceCounter == 0) spaceCounter += 4;
    spaceCounter++;
    while (indexor > 0) {
        // Check if space is needed
        spaceCounter--;
        if (spaceCounter == 0) {
            spaceCounter = 4;
            cout << " ";
        }
        // Print binary digit
        cout << (num & indexor ? '1' : '0');
        indexor = indexor >> 1;
    }
}

#define VERBOSE 1

void processBuffer(uint64_t* bufferPointer, uint8_t bufferActive, uint32_t* checkSize) {
    #ifdef VERBOSE
    cout << "       buffer = " << *bufferPointer << endl;
    cout << "       buffer = ";
    printBin(*bufferPointer, 64);
    cout << endl;
    printf( " bufferActive = %d\n", bufferActive);
    cout << "   check size = " << *checkSize << endl;
    cin.ignore();   // Wait for user to press enter
    #endif



}

void sendImage() {
    // Initialise buffer related variables
    uint64_t buffer = 0;
    uint32_t checkSize = 1;
    // Variable to note how many bits of the buffer are currently in use
    uint8_t bufferActive = 0;
    // For each pointer in the encoded pointer array
    for (uint16_t pointerNumber = 0; pointerNumber <= ENCODING_ARRAYS_USED; pointerNumber++) {
        uint16_t *dataPointer = dataPointers[pointerNumber];
        // Increment this pointer to get all data from this array
        for (uint16_t arrayPosition = 0; arrayPosition <= ARRAY_SIZE - 1; arrayPosition++) {
            // Add the next two bytes to the buffer
            buffer = buffer << 16;
            buffer += *dataPointer;
            bufferActive += 16;
            // Process the buffer NOTE: May also need a 'total pixels printed' kinda variable
            processBuffer(&buffer, bufferActive, &checkSize);
            // Increment the data pointer
            dataPointer++;
        }
    }

}

int main() {
    setup();

    // sendImage();

    // binary print test
    printBin(0b111100001010, 12);
    printf("\n");
    printBin(0b0111100001010, 13);
    printf("\n");
    printBin(0b10111100001010, 14);
    printf("\n");
    printBin(0b110111100001010, 15);
    printf("\n");
    printBin(0b0110111100001010, 16);
    printf("\n");

    // // test
    // uint64_t buffer = 0b01011;
    // uint8_t bufferActive = 5;
    // uint16_t newData = 0b1111000011111111;
    // buffer = buffer << 16;
    // buffer += newData;
    // cout << buffer << endl;

    return 0;
}