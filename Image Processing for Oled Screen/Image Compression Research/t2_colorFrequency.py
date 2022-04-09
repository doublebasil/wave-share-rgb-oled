from matplotlib import pyplot
from PIL import Image
from math import pow

"""
This test plots colour against frequency
This was very insightful; it shows that in most 128x 128 images, most of the possible 
colors aren't ever used!
I've realised that for 128x128 image, even if every single pixel has a different
colour, there will still only be 16384 colours used (out of a possible 65536 with
16 bit colours).
This seems to me to be good evidence that huffman coding could be an effective method 
to compress pixelated images for use on arduino.
"""

def rgb256To565(rgb):
    return (round(rgb[0] * (31 / 255)), round(rgb[1] * (63 / 255)), round(rgb[2]) * (31 / 255))

def rgb565To16Bit(rgb):
    return int((rgb[0] << 11) + (rgb[1] << 5) + rgb[2])

def main():
    im = Image.open('pic3.png')
    rgbData = list(im.getdata())

    # Fill data with 0s
    data = []
    for i in range(0, int(pow(2, 16))):
        data.append(0)

    for pixel in rgbData:
        value = rgb256To565(pixel)
        value = rgb565To16Bit(value)
        data[value] = data[value] + 1

    numColorsUnused = 0
    for i in data:
        if i == 0:
            numColorsUnused += 1
    print("There are " + str(numColorsUnused) + " colors that aren't used!")    

    sortedData = data.copy()
    sortedData.sort()

    pyplot.subplot(1, 2, 1)
    pyplot.plot(data)
    pyplot.subplot(1, 2, 2)
    pyplot.plot(sortedData)
    pyplot.show()

if __name__ == "__main__":
    main()