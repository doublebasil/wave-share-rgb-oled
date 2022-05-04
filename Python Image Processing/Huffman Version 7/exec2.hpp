#include <stdint.h>
#include "image.h"

class ImageSender 
{
    private:
        uint16_t x;
        uint16_t y;
        void getHuffInput(uint16_t* codeNumber, uint8_t checkSize, uint32_t* output);
        void getHuffOutput(uint16_t* codeNumber, uint8_t checkSize, uint16_t* output);
        void processBuffer(uint64_t* bufferPointer, uint8_t* bufferActive, uint8_t* checkSize, uint32_t* sentBytes);
    public:
        ImageSender();
        int send();
};