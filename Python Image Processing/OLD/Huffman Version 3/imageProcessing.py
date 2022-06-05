"""
This code uses imagemagick from a bash terminal to resize an image 
 and reduce the colours to RGB565 for the WaveShare oled

Requirements:
- PIL (python image library) using pip, this should be preinstalled
- You have installed imagemagick ready to use within a terminal

The following imagemagick command is used

convert inputImage.jpg -resize 128x128 -ordered-dither threshold,32,64,32 output.png

"""

import os               # For using imagemagick and viewing files
from PIL import Image   # For opening png to view data

def getImageData():
    # Check if imagemagick is installed
    r = os.system('convert -help 1>/dev/null')
    if r == 32512:
        exit("\nError - Looks like imagemagick is not installed")
        
    # Get a list of files in the current directory
    fileList = os.listdir()
    # Here is a list of image file extensions
    imageExtensions = ['.jpg', '.jpeg', '.png']
    # Within fileList, filter out non-image files
    imageList = []
    for filename in fileList:
        # Seperate file name from extension
        extension = os.path.splitext(filename)[1]
        # If the file has an image extension, keep it
        if extension in imageExtensions:
            imageList.append(filename)
    # Give an error if imageList is empty
    if len(imageList) == 0:
        exit("\nError - Found no images in current directory")
    
    # We now have a list of images, ask user which one to use
    print("Type number of image to use")
    counter = 0
    for imageName in imageList:
        counter += 1
        print(str(counter) + " - " + imageName)
    userInput = int(input("Image Number = "))
    if (userInput <= 0) or (userInput > counter):
        exit("\nError - Invalid number")
    
    # Ask for oled Width and Height
    displayWidth = int(input("What is your oled display's width? "))
    if displayWidth <= 0:
        exit("Error - invalid display width")
    displayHeight = int(input("What is your oled display's height? "))
    if displayHeight <= 0:
        exit("\nError - invalid display width")
    
    # Need to create a filename for the temporary image name, this cannot be
    # the same filename as a pre-existing file as this would overwrite
    for attempt in range(0, 100):
        tempFilename = "temp" + str(attempt) + ".png"
        if not (tempFilename in fileList):
            # Success (providing I wrote the code properly haha)
            break
    
    # Construct the imagemagick command
    inputFilename = imageList[counter - 1]
    command = "convert " + inputFilename
    command += " -resize \"" + str(displayWidth) + "x" + str(displayHeight) + "!\""
    command += " -ordered-dither threshold,32,64,32"
    command += " " + tempFilename
    # Execute the command
    os.system(command)

    # Now get the RGB data from the temp image
    rawImageData = Image.open(tempFilename)
    rgb256Data = list(rawImageData.getdata())
    rgb565Data = []
    for pixel in rgb256Data:
        rgb565Data.append(_convertToRGB565(pixel[0], pixel[1], pixel[2]))

    # Remove the temporary png file
    os.system("gio trash " + tempFilename)

    # Return the 
    return rgb565Data


def _convertToRGB565(r, g, b):
    # Colours are initially 0 to 255, need to reduce range
    red = round((r * 31) / 255)     # Reduce to 5 bit (0 to 32)
    green = round((g * 63) / 255)   # Reduce to 6 bit (0 to 64)
    blue = round((b * 31) / 255)    # Reduce to 5 bit (0 to 32)
    # Bitshift each value to fit to the RGB565 format: RRRRR GGGGGG BBBBB
    green = green << 5
    red = red << (5 + 6)
    # You can now add them and conver to hex
    rgb565 = hex(red + green + blue)
    # Need to ensure that it has 4 digits, remove the 0x from the start
    rgb565 = rgb565[2:len(rgb565)]
    while len(rgb565) < 4:
        # Add 0 to the front until there are 4 digits (16 binary bits)
        rgb565 = "0" + rgb565
    # Now add the 0x back to the start and return this value
    rgb565 = "0x" + rgb565
    return rgb565

