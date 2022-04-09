#include <iostream>
#include <typeinfo>

using namespace std;

int main(void) {
    int a[] = {1, 2, 3, 4};

    int b = 10;
    int* b_p = &b;

    unsigned long g;

    cout << typeid(g).name() << endl;

    return 0;
}