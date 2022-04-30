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
    uint64_t indexor = (uint64_t) 1 << (bits - 1);
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

// for testing in main we have getHuffInput(3, 6);
void getHuffInput(uint16_t codeNumber, uint8_t checkSize) {
    // If codeNumber = 6 and checkSize = 3, this function will return the 
    // 7th (6 + 1)th 'input code' with length of 3
    
    // Some error testing don't mind me
    // cout << binCodeSizes[checkSize-1] << endl << endl;
    if (codeNumber > binCodeSizes[checkSize-1]) {
        cout << "codeNumber looks to be invalid :/" << "\n";
        exit(1);
    }

    // Find what binary digit we want to start at e.g. we want to start at the 76th digit
    uint32_t wantedDigit = 0;
    for (uint8_t index = 0; index < (checkSize - 1); index++) {
        wantedDigit += binCodeSizes[index] * (index + 1);
        // cout << binCodeSizes[index] << endl;
    }
    wantedDigit += codeNumber * checkSize;

    cout << "In total we want to start at this binary digit:" << wantedDigit << "\n";

    // Find where in the data we need to go for this 'wantedDigit'
    uint16_t pointerIndex = 0;
    uint16_t elementIndex = 0;
    while (wantedDigit > ARRAY_SIZE * 16) {
        pointerIndex++;
        wantedDigit -= ARRAY_SIZE * 16;
    }
    while (wantedDigit > 16) {
        elementIndex++;
        wantedDigit -= 16;
    }
    cout << "pointerIndex  = " << pointerIndex << "\n";
    cout << "elementIndex  = " << elementIndex << "\n";
    cout << "wantedDigit   = " << wantedDigit << "\n";

    // Need to get an indexor kinda variable from wantedDigit
    uint16_t binaryIndexor = 1;
    binaryIndexor = (uint16_t) binaryIndexor << (16 - wantedDigit);
    cout << "binaryIndexor = ";
    printBin(binaryIndexor, 16);
    cout << "\n";

    // Now get the digits I guess
    // Need to obtain checkSize number of digits
    uint8_t digitsObtained = 0;
    uint32_t output = 0;

    // Attempt 1
    uint16_t* ptr = huffInput[pointerIndex];
    for (int e = 0; e < elementIndex; e++) {
        ptr++;
    }
    cout << "ptr is initially pointing to " << (*ptr) << "\n";
    while (true) {
        // Add data to the output
        output << 1;
        output += ((*ptr & binaryIndexor) > 1);
        // Increment digitsObtained
        digitsObtained++;
        if (digitsObtained == checkSize) break;
        // Increment counters related to binary stuff
        binaryIndexor = (uint16_t) binaryIndexor >> 1;
        if (binaryIndexor == 0) {
            binaryIndexor = (uint16_t) 1 << 15;
            elementIndex++;
            // If we have ran out of elements in this array, we'll need to use the next one
            // I GUESS THIS SHOULD WORK THE SAME WAY IF THIS IS THE LAST ARRAY? BECAUSE THAT SHOULDN'T HAPPEN
            if (elementIndex == ARRAY_SIZE) {
                pointerIndex++;
                ptr = huffInput[pointerIndex];
            }
            else {
                ptr++;
            }
        }
    }

    printBin(output, checkSize);
    cout << "\n";

}

void processBuffer(uint64_t* bufferPointer, uint8_t bufferActive, uint8_t* checkSize) {
    #ifdef VERBOSE
    cout << "       buffer = " << *bufferPointer << endl;
    cout << "       buffer = ";
    printBin(*bufferPointer, 64);
    cout << endl;
    printf( " bufferActive = %d\n", bufferActive);
    cout << "   check size = " << *checkSize << endl;
    cout << " --- Press enter --- ";
    cin.ignore();   // Wait for user to press enter
    #endif

    // #include <brainf.h>

    // Keep increasing checkSize until it exceeds the bufferActive size
    while (checkSize - bufferActive >= 0) {
        // Check all the codes of this size
        for (uint16_t codeNumber = 0; codeNumber <= binCodeSizes[*checkSize]; codeNumber++) {
            
        }
    }


}

void sendImage() {
    // Initialise buffer related variables
    uint64_t buffer = 0;
    uint8_t checkSize = 1;
    // Variable to note how many bits of the buffer are currently in use
    uint8_t bufferActive = 0;
    // For each pointer in the encoded pointer array
    for (uint16_t pointerNumber = 0; pointerNumber <= ENCODING_ARRAYS_USED; pointerNumber++) {
        uint16_t *dataPointer = dataPointers[pointerNumber];
        // Increment this pointer to get all data from this array
        for (uint16_t arrayPosition = 0; arrayPosition <= ARRAY_SIZE - 1; arrayPosition++) {
            // Add the next two bytes to the buffer
            buffer = (uint64_t) buffer << 16;
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


    getHuffInput(3, 6);

    // const unsigned char a = 1;
    // signed char b = 2;
    // if (a == b) {
    //     cout << "yes" << endl;
    // } else {
    //     cout << "no" << endl;
    // }
    
    // printBin(43690, 16);
    // cout << endl;
    // printBin(43690, 64);
    // cout << endl;

    // // binary print test
    // printBin(0b111100001010, 12);
    // printf("\n");
    // printBin(0b0111100001010, 13);
    // printf("\n");
    // printBin(0b10111100001010, 14);
    // printf("\n");
    // printBin(0b110111100001010, 15);
    // printf("\n");
    // printBin(0b0110111100001010, 16);
    // printf("\n");

    // // test
    // uint64_t buffer = 0b01011;
    // uint8_t bufferActive = 5;
    // uint16_t newData = 0b1111000011111111;
    // buffer = buffer << 16;
    // buffer += newData;
    // cout << buffer << endl;

    return 0;
}
