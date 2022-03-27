"""
This code will only work on Linux distributions
You must have imagemagick installed and ready to use from the command line
On debian distros, sudo apt install imagemagick

The following commmand from imagemagick converts the image to a 128x128 png
with RGB565 color depth

convert inputImage.jpg -resize 128x128 -ordered-dither threshold,32,64,32 output.png

Python is then used to create a load of text to paste into your arduino file,
which can then be loaded onto the screen

"""

import os
    
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

if __name__ == '__main__':
    main()
