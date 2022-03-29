from PIL import Image

"""
The idea here was that we normally send pixels in rows then columns.
My idea was that we have e.g. 5 pixels in a row that are the same color,
instead of having 5 of the same value we'd just have 2 bytes for the color,
and 1 byte to say repeat this 5 times. 
This unfortunately increases the size of an image massively rather than
shrinking it. This is because of the gradients across the images, meaning
there aren't many blocks of pixels that are exactly the same color
"""

def main():
    im = Image.open('128x128.png')
    
    rgbData = list(im.getdata())
    print("Currently uses                        " + str(2 * len(rgbData)) + " bytes")

    counter = 0
    for i in range(1, len(rgbData)):
        if rgbData[i - 1] != rgbData[i]:
            counter += 1
    print("With your line compression, we'd need " + str(counter * 3) + " bytes")


if __name__ == '__main__':
    main()