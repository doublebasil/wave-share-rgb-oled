from PIL import Image
from math import pow

"""
Attempting to use huffman coding to compress images
"""

def rgbTo16Bit(rgb):
    return (rgb[0] << 11) + (rgb[1] << 5) + rgb[2]

def main():
    im = Image.open('128x128.png')
    
    rgbData = list(im.getdata())






if __name__ == '__main__':
    # main()
    print(rgbTo16Bit((31, 63, 31)))
    print(pow(2, 16) - 1)