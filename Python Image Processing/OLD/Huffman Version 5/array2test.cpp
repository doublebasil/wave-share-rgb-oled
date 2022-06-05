#include <iostream>
#include "image.h"

using namespace std;

int main(void) {
    cout << hex;
    for (int i = 0; i <= array2Size; i++) {
        cout << i << " -> " << hex << array2Idk[i] << dec << endl;
    }
    
    cout << "---" << endl;

    cout << "Actual size of array 2 is " << sizeof(array2Idk) / sizeof(array2Idk[0]) << endl;
    // cout << hex;
    // cout << array2Idk[(sizeof(array2Idk)/sizeof(array2Idk[0]))-2] + " ";
    // cout << array2Idk[(sizeof(array2Idk)/sizeof(array2Idk[0]))-1] << dec << endl;

    
    return 0;
}