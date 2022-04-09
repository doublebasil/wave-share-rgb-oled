"""
Requirements:
- You are using Linux (so that imagemagick can be used from a terminal)
- PIL (python image library) using pip, this should be preinstalled
- You have installed imagemagick ready to use within a terminal

The following commmand from imagemagick converts the image to a 128x128 png
with RGB565 color depth

convert inputImage.jpg -resize 128x128 -ordered-dither threshold,32,64,32 output.png

Python is then used to create a load of text to paste into your arduino file,
which can then be loaded onto the screen

"""

import os               # For using imagemagick and viewing files
from PIL import Image   # For opening png to view data

from time import sleep
    
def main():
    # Check if imagemagick is installed
    r = os.system('convert -help 1>/dev/null')
    if r != 0:
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
    displayWidth = int(input("\nWhat is your oled display's width? "))
    if displayWidth <= 0:
        exit("Error - invalid display width")
    displayHeight = int(input("\nWhat is your oled display's height? "))
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
    command += " -resize " + str(displayWidth) + "x" + str(displayHeight)
    command += " -ordered-dither threshold,32,64,32"
    command += " " + tempFilename
    # Execute the command
    os.system(command)
    
    # Now need to convert that image to text you can copy
    # If image.h already exists, delete it
    if "image.h" in fileList:
        os.system('gio trash image.h')
    # Use Python Image Library to get the image data
    tempImageData = Image.open(tempFilename)
    # Use the image data as a list of RGB values, these are 0 to 255
    rgbData = list(tempImageData.getdata())
    # Create an image.h file to write to
    with open('image.h', 'w') as outputFile:
        # Include the stdint.h header file
        outputFile.write("#include <stdint.h>\n\n")
        outputFile.write("int imageData[] = {")
        # Counter for deciding when to create a new line
        newLineCounter = 0
        # Counter for remembering how many pixels have been added
        pixelCounter = 0
        # For each RGB value
        for currentRgbValue in rgbData:
            # Convert the RGB value to a RGB565 hex code
            rgb565 = convertToRGB565(currentRgbValue[0], currentRgbValue[1], currentRgbValue[2])
            # Write this hex code to the file
            outputFile.write(rgb565)
            pixelCounter += 1
            # If this isn't the last value, add a comma after the hex value
            print(str(pixelCounter) + ", " + str(displayHeight * displayWidth))
            if pixelCounter != ((displayWidth * displayHeight) - 1):
                outputFile.write(", ")
            # Check how many values we have on this one line
            newLineCounter += 1
            if newLineCounter >= 6:
                outputFile.write("\n\t")
                newLineCounter = 0
        # End the array 
        outputFile.write("};")

    # Finally, remove the temporary png file
    os.system("gio trash " + tempFilename)

        # for i in rgbData:
        #     print(i)
        #     sleep(0.5)

def convertToRGB565(r, g, b):
    # Colours are initially 0 to 255, need to reduce range
    red = round((r * 32) / 255)     # Reduce to 5 bit (0 to 32)
    green = round((g * 64) / 255)   # Reduce to 6 bit (0 to 64)
    blue = round((b * 32) / 255)    # Reduce to 5 bit (0 to 32)
    # Bitshift each value to fit to the RGB565 format: RRRRR GGGGGG BBBBB
    green = green << 5
    red = red << (5 + 6)
    # You can now add them and conver to hex
    rgb565 = hex(red + green + blue)
    # Need to ensure that it has 4 digits, remove the 0x from the start
    rgb565 = rgb565[2:len(rgb565)]
    while len(rgb565) < 4:
        # Add 0 to the front until there are 4 digits
        rgb565 = "0" + rgb565
    # Now add the 0x back to the start and return this value
    rgb565 = "0x" + rgb565
    return rgb565

if __name__ == '__main__':
    main()
