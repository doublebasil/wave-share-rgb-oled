import os

# Some setting constants here
BYTES_PER_LINE = 4          # This changes how the file is written, no effect on performance
BYTES_LOADED_AT_ONCE = 50   # Greater number here increases RAM usage but may decrease storage space usage

def generateHeaderFile(huffmanTable, encodedData):
    # Get length of encodedData
    dataLength = len(encodedData)
    # Get a list of files currently in the directory
    fileList = os.listdir()
    # Check if there is already a file called 'image.h'
    if 'image.h' in fileList:
        # Ask the user if it can be deleted
        uinput = input("A file called 'image.h' already exists.\nType 'y' to overwrite it: ")
        if str(uinput) == "y":
            os.system('gio trash image.h')
        else:
            return 1
    # Create a new header.h file
    with open('image.h', 'w') as file:
        # Add stdint.h to the header file
        file.write("#include <stdint.h>\n\n")

        # Now add all the encoded image data
        file.write("uint16_t encodedImage[] = {")
        # Counter to remember when to add a new line
        newLineCounter = 0
        # Add a pixel counter to know when we have printed all the bytes
        pixelCounter = 0
        # Now add all the bytes
        for b in encodedData:
            # Write that byte to the header file
            file.write(b)
            # Increment the counters
            pixelCounter += 1
            newLineCounter += 1
            # If this isn't the last byte then add a comma
            if pixelCounter != dataLength:
                file.write(", ")
            # Check if we need a new line
            if newLineCounter >= BYTES_PER_LINE:
                file.write("\n\t")
                newLineCounter = 0
        # End the array
        file.write("};")