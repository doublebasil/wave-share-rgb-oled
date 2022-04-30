#include <iostream>
#include <stdint.h>
#include "image.h"

using namespace std;

int main() {
    /*
        [X      X]
    [12   5]  [X   3]
             [1 2]    
    */

    /*
    We've got an array containg some pointers, some pointers to pointers, and some pointers to pointers to pointer
    and that is messy. I think we can reduce this to 3 arrays:
    1) Number of each binary size we have, so for the above table, [0, 3, 2]?
    2) All the binary numbers we have, so for the above table: [000111100101]
                                                                XX  XX   XXX
    3) The values of each binary code in order that they occur in the above array [12, 5, 3, 1, 2]
    */

    // uint16_t num2_1 = 12;
    // uint16_t num2_2 = 5;
    // uint16_t num2_4 = 3;
    // uint16_t num3_5 = 1;
    // uint16_t num3_6 = 2;

    // uint16_t *layer3_3[] = {&num3_5, &num3_6};
    // uint16_t *layer2_2[] = {&layer3_3[0], &num2_4};
    // uint16_t *layer2_1[] = {&num2_1, &num2_2};
    // uint16_t **layer1_1[] = {&layer2_1[0], &layer2_2[0]};

    // // uint16_t* layer3_1
    // // uint16_t* layer3_2
    // uint16_t* layer3_3 = 2;
    // // uint16_t* layer3_4

    // uint16_t* currentPointer = dataPointers[0];
    // for (int i = 0; i <= 4; i++) {
    //     cout << *currentPointer << endl;
    //     currentPointer++;
    // }


    // uint8_t a = 12;
    // uint8_t *ap = &a;

    // cout << sizeof(a) << endl;
    // cout << sizeof(ap) << endl;


    // return 0;
}