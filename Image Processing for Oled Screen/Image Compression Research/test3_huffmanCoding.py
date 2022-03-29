from PIL import Image
from math import pow

"""
Attempting to use huffman coding to compress images

Thoughts:
    in c I could implement the huffman table with pointers and 1x2 arrays
    in python I could implement the table with 1x2 lists within list

    Making the table is gonna be a brainf

"""

def rgbTo16Bit(rgb):
    return (rgb[0] << 11) + (rgb[1] << 5) + rgb[2]

def main():
    im = Image.open('128x128.png')
    
    rgbData = list(im.getdata())

    




if __name__ == '__main__':
    # main()

    # print(rgbTo16Bit((31, 63, 31)))
    # print(pow(2, 16) - 1)

    # This does sort by only the first column, which is good
    a = [[2, 'b'], [3, 'c'], [1, 'a'], [0, 'j']]
    a.sort()
    print(a)