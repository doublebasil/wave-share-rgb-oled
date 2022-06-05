#include <stdint.h>

#include "ws_oled.hpp"

class WSImageSender: public WSOled {
    protected:
        uint16_t x;
        uint16_t y;
        void sendPixel(uint16_t* x, uint16_t* y, uint16_t* pixelData);
        void getHuffInput(uint16_t* codeNumber, uint8_t checkSize, uint32_t* output);
        void getHuffOutput(uint16_t* codeNumber, uint8_t checkSize, uint16_t* output);
        void processBuffer(uint64_t* bufferPointer, uint8_t* bufferActive, uint8_t* checkSize, uint32_t* sentBytes, uint16_t* x_ptr, uint16_t* y_ptr);
    public:
        WSImageSender();
        // Could potentially add a startx and starty to the send function, for images that don't fill the display
        int sendImage();
};
