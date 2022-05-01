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

void getHuffInput(uint16_t codeNumber, uint8_t checkSize, uint32_t* output) {
    // If codeNumber = 6 and checkSize = 3, this function will return the 
    // 7th (6 + 1)th 'input code' with length of 3
    
    // Some error testing don't mind me
    if (codeNumber >= binCodeSizes[checkSize-1]) {
        cout << "codeNumber looks to be invalid :/" << "\n";
        exit(1);
    }
    // Find what binary digit we want to start at e.g. The code we want might start at the 76th binary digit
    uint32_t wantedDigit = 0;
    for (uint8_t index = 0; index < (checkSize - 1); index++) {
        wantedDigit += binCodeSizes[index] * (index + 1);
        // cout << binCodeSizes[index] << endl;
    }
    wantedDigit += codeNumber * checkSize;
    wantedDigit++;
    // The data is stored in 16 bit elements within arrays
    uint16_t pointerIndex = 0;  // Which array is needed
    uint16_t elementIndex = 0;  // Which element within the array is needed
    // wantedDigit is the digit within the element that's needed
    // Use wantedDigit to find which array and which element is needed
    while (wantedDigit > ARRAY_SIZE * 16) {
        pointerIndex++;
        wantedDigit -= ARRAY_SIZE * 16;
    }
    while (wantedDigit > 16) {
        elementIndex++;
        wantedDigit -= 16;
    }
    // Use wanted digits to create a 'binaryIndexor' variable
    // e.g. if wantedDigit = 3, binaryIndexor = 0010 0000 0000 0000
    uint16_t binaryIndexor = 1;
    binaryIndexor = (uint16_t) binaryIndexor << (16 - wantedDigit);
    // Now use the binaryIndexor, elementIndex and pointerIndex to get each binary digit from the code, one by one
    // NOTE: YOU SHOULD IMPLEMENT A MORE EFFICIENT METHOD WHERE THE DIGITS ARE OBTAINED IN GROUPS, NOT ONE AT A TIME
    // Variable to to know when we have found enough digits
    uint8_t digitsObtained = 0;
    // // The function's output variable
    // uint32_t output = 0;
    // Create a pointer and increment it to the element that is needed
    uint16_t* ptr = huffInput[pointerIndex];
    for (int i = 0; i < elementIndex; i++) {
        ptr++;
    }
    // While loop is broken when digitsObtained == checkSize
    while (true) {
        // Bitshift the output to make room for the next bit
        *output = (uint32_t) *output << 1;
        // Add the next bit by using a bitwise 'and' with the binaryIndexor
        *output += ((*ptr & binaryIndexor) != 0);
        // Increment digitsObtained
        digitsObtained++;
        // Check if the process is completed
        if (digitsObtained == checkSize) break;
        // The second half of the while loop bitshifts the binaryIndexor
        binaryIndexor = (uint16_t) binaryIndexor >> 1;
        // If the binaryIndexor is now 0, we have ran out of digits in this element
        if (binaryIndexor == 0) {
            // Set the binaryIndexor to the start of the element
            binaryIndexor = (uint16_t) 1 << 15;
            // Move to the next element within the array
            elementIndex++;
            // If we have ran out of elements in this array, use the next array
            // Note: This code doesn't check that you are going out of bounds in any of the arrays, because that shouldn't happen anyway
            if (elementIndex == ARRAY_SIZE) {
                // Move to the next array
                pointerIndex++;
                // Update the pointer
                ptr = huffInput[pointerIndex];
            }
            // If we haven't ran out of elements, just use the next element by incrementing the pointer
            else {
                ptr++;
            }
        }
    }
}

#define VERBOSE 1

void processBuffer(uint64_t* bufferPointer, uint8_t bufferActive, uint8_t* checkSize) {
    #ifdef VERBOSE
    cout << "       buffer = " << *bufferPointer << endl;
    cout << "       buffer = ";
    printBin(*bufferPointer, 64);
    cout << endl;
    printf( " bufferActive = %d\n", bufferActive);
    printf("   check size = %d\n", *checkSize);
    cout << " --- Press enter --- ";
    cin.ignore();   // Wait for user to press enter
    #endif

    // #include <brainf.h>

    // Keep increasing checkSize until it exceeds the bufferActive size
    while (checkSize - bufferActive >= 0) {
        // Check all the codes of this size
        for (uint16_t codeNumber = 0; codeNumber <= binCodeSizes[*checkSize]; codeNumber++) {
            // Idk, work your code magic in here or someth
            exit(420420);
        }
        // If it wasn't found, increase the checkSize
        checkSize++;

        printBin((uint64_t) *bufferPointer >> (bufferActive - *checkSize), 64);
        printf("\n");
        exit(420);
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

    sendImage();



    // getHuffInput(386, 14);
    // cout << endl;
    // getHuffInput(387, 14);
    // cout << endl;

    // getHuffInput(388, 14);
    // cout << endl;

    // uint32_t answer;
    // for (unsigned char i = 0; i < maxBinCodeLen; i++) {
    //     // if (i == 7) break;
    //     for (unsigned short j = 0; j < binCodeSizes[i]; j++) {
    //         getHuffInput(j, i + 1, &answer);
    //         // printf("%d, %d -> ", i + 1, j);
    //         // getHuffInput(j, i + 1);
    //         printBin(answer, i + 1);
    //         cout << endl;
    //     }
    // }

    // getHuffInput(3, 6);

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
