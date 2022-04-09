from machine import Pin, SPI
from utime import sleep

CS = 2
DC = 3
RST = 4
DISPLAY_HEIGHT = 128
DISPLAY_WIDTH = 128
BAUD=115200

"""
  Screen Name      |     uC Name      |  Pin Number
  _________________|__________________|______________
  Chip Select   CS |   e.g. GPIO2     |   e.g. 4
  Data/Command  DC |   e.g. GPIO3     |   e.g. 5
  Reset        RST |   e.g. GPIO4     |   e.g. 6
                   |                  |
               DIN | MOSI aka SPIx_RX |     21
               CLK |  SCK aka SPIxSCK |     24
               
"""

class WaveShareOled():
    
    def smallDelay(self):
        sleep(0.01)
    
    def oledWriteReg(self, reg):
        # Convert reg to byte data type
        regByte = bytes([reg])
        self.DC(0)
        self.CS(0)
        self.spi.write(regByte)
        self.CS(1)
        
    def oledWriteData(self, data):
        # Convert data to byte data type
        dataByte = bytes([data])
        self.DC(1)
        self.CS(0)
        self.spi.write(dataByte)
        self.CS(1)
    
    def clear(self):
        self.oledWriteReg(0x15);
        self.oledWriteData(0);
        self.oledWriteData(127);
        self.oledWriteReg(0x75);
        self.oledWriteData(0);
        self.oledWriteData(127);
        
        self.oledWriteReg(0x5C);
        
        for i in range(self.displayWidth * self.displayHeight * 2):
            # print(str(i / (self.displayWidth * self.displayHeight * 2)))
            self.oledWriteData(0x50);
    
    def begin(self, CS, DC, RST, displayWidth, displayHeight, baudrate):
        self.CS = Pin(CS, Pin.OUT, value=0)
        self.DC = Pin(DC, Pin.OUT, value=0)
        self.RST = Pin(RST, Pin.OUT, value=0)
        
        self.displayHeight = displayHeight
        self.displayWidth = displayWidth
        self.baudrate = baudrate
        
        # The polarity and phase are the same as SPI_MODE3
        # The pico has room for 2 SPI devices, we will use pins labelled 0
        self.spi = SPI(0, baudrate=self.baudrate, polarity=1, phase=1, bits=8, firstbit=SPI.MSB)
        
        # Reset the display by setting RST pin low
        self.RST(1)
        sleep(0.1)
        self.RST(0)
        sleep(0.1)
        self.RST(1)
        sleep(0.1)
       
        # Now for some inexplicable magic from the manufacturer
        self.oledWriteReg(0xFD)  # Command lock
        self.oledWriteData(0x12)
        self.oledWriteReg(0xFD)  # Command lock
        self.oledWriteData(0xB1)

        self.oledWriteReg(0xAE)  # Display off
        self.oledWriteReg(0xA4)  # Normal Display mode

        self.oledWriteReg(0x15)  # Set column address
        self.oledWriteData(0x00) # Column address start 00
        self.oledWriteData(0x7F) # Column address end 127
        self.oledWriteReg(0x75)  # Set row address
        self.oledWriteData(0x00) # Row address start 00
        self.oledWriteData(0x7F) # Row address end 127    

        self.oledWriteReg(0xB3)
        self.oledWriteData(0xF1)

        self.oledWriteReg(0xCA)  
        self.oledWriteData(0x7F)

        self.oledWriteReg(0xA0)  # Set re-map & data format
        self.oledWriteData(0x74) # Horizontal address increment

        self.oledWriteReg(0xA1)  # Set display start line
        self.oledWriteData(0x00) # Start 00 line

        self.oledWriteReg(0xA2)  # Set display offset
        self.oledWriteData(0x00)

        self.oledWriteReg(0xAB)  
        self.oledWriteReg(0x01)  

        self.oledWriteReg(0xB4)  
        self.oledWriteData(0xA0)   
        self.oledWriteData(0xB5)  
        self.oledWriteData(0x55)    

        self.oledWriteReg(0xC1)  
        self.oledWriteData(0xC8) 
        self.oledWriteData(0x80)
        self.oledWriteData(0xC0)

        self.oledWriteReg(0xC7)  
        self.oledWriteData(0x0F)

        self.oledWriteReg(0xB1)  
        self.oledWriteData(0x32)

        self.oledWriteReg(0xB2)  
        self.oledWriteData(0xA4)
        self.oledWriteData(0x00)
        self.oledWriteData(0x00)

        self.oledWriteReg(0xBB)  
        self.oledWriteData(0x17)

        self.oledWriteReg(0xB6)
        self.oledWriteData(0x01)

        self.oledWriteReg(0xBE)
        self.oledWriteData(0x05)

        self.oledWriteReg(0xA6)

        sleep(0.2)
        # End of nonsense code
        
        # Turn on the display
        self.oledWriteReg(0xAF)
        
        sleep(0.5)
        
        self.clear()
        
        return 0
    
    def setPixel(self, x, y, color):
        self.oledWriteReg(0x15)
        self.oledWriteData(x)
        self.oledWriteData(x)
        self.oledWriteReg(0x75)
        self.oledWriteData(y)
        self.oledWriteData(y)
        # fill!
        self.oledWriteReg(0x5C)
        # The 16 bits are sent in two seperate bytes
        self.oledWriteData(color >> 8)
        self.oledWriteData(color - ((color >> 8) << 8))
        

oled = WaveShareOled()

def main():
    print("Starting")
    oled.begin(CS, DC, RST, DISPLAY_WIDTH, DISPLAY_HEIGHT, BAUD)
    print("Completed setup")
    
    for x in range(5, 20):
        for y in range(5, 20):
            oled.setPixel(x, y, 0x2222)

main()