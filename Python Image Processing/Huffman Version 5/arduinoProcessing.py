from asyncio.base_futures import _FINISHED
import os
from math import ceil

from numpy import number

# Some setting constants here
BYTES_PER_LINE = 4      # This changes how the file is written, no effect on performance
BYTES_PER_BATCH = 50    # Greater number here MIGHT increases RAM usage and decrease storage space usage? Idk yet

def generateHeaderFile(huffmanTable, encodedData):

    # Some code for storing the Huffman table
    # My (potentially sub-optimum) method will create 3 arrays to store
    # the Table data
    # 1 - Number of each length of binary number in Huffman Code
    # 2 - All the huffman codes in a long binary list, seperated into
    #     an array of uint16_t (probably)
    # 3 - The values that each binary code represent, in order 
    #     corresponding to array 2
    # ---
    # Collect data for array 1
    binCodeLenFreq = []
    currentLength = 0
    for row in huffmanTable:
        binaryCode = row[0]
        binaryCodeLen = len(binaryCode)
        while currentLength < binaryCodeLen:
            binCodeLenFreq.append(0)
            currentLength += 1
        binCodeLenFreq[currentLength-1] += 1
    # print(huffmanTable)
    # print(binCodeLenFreq)

    # Now code for actually making the header file
    # Get length of encodedData
    dataLength = len(encodedData)
    # Get a list of files currently in the directory
    fileList = os.listdir()
    # Check if there is already a file called 'image.h'
    if 'image.h' in fileList:
        # Ask the user if it can be deleted
        # uinput = input("A file called 'image.h' already exists.\nType 'y' to overwrite it: ")
        print("A file called 'image.h' already exists.\nType 'y' to overwrite it: y")
        uinput = "y"
        if str(uinput) == "y":
            os.system('gio trash image.h')
        else:
            return 1
    # Create a new header.h file
    with open('image.h', 'w') as file:
        # Add stdint.h to the header file
        file.write("#include <stdint.h>\n\n")
        # Add comment
        file.write("// Encoded data for the image \n\n")

        # Gonna struggle to comment this junk
        numberOfBatches = ceil(len(encodedData) / BYTES_PER_BATCH)
        bytesInLastBatch = len(encodedData) % BYTES_PER_BATCH
        for batchNumber in range(0, numberOfBatches):
            file.write("uint16_t dataBatch" + str(batchNumber) + "[] = {")
            # Add a counter for remembering when to add new lines
            newLineCounter = 0
            # Add a pixel counter to know when we have printed all the bytes
            pixelCounter = 0
            for b in encodedData[batchNumber * BYTES_PER_BATCH : (batchNumber + 1) * BYTES_PER_BATCH]:
                # Write that byte to the header file
                file.write(b)
                # Increment the counters
                pixelCounter += 1
                newLineCounter += 1
                # If this is our last batch
                if batchNumber == numberOfBatches - 1:
                    # If this isn't our last byte then add a comma
                    if pixelCounter != bytesInLastBatch:
                        file.write(", ")
                else:
                    # If this isn't our last byte then add a comma
                    if pixelCounter != BYTES_PER_BATCH:
                        file.write(", ")
                # Check if we need a new line
                if newLineCounter >= BYTES_PER_LINE:
                    file.write("\n\t")
                    # Reset the new line counter
                    newLineCounter = 0
            
            # End the array
            file.write("};\n\n")

        # Now need to create the array of pointers
        file.write("// Array of pointers \n\n")
        file.write("uint16_t* dataPointers[] = {")
        # Add newLineCounter
        newLineCounter = 0
        # For each batch, add a pointer to that batch
        for batchNumber in range(0, numberOfBatches):
            # Add a pointer
            file.write("&dataBatch" + str(batchNumber) + "[0]")
            # Increment the newLineCounter
            newLineCounter += 1
            # Add a comma if necessary
            if batchNumber != (numberOfBatches - 1): file.write(", ")
            # Add a new line if necessary
            if newLineCounter >= BYTES_PER_LINE: 
                file.write("\n\t")
                newLineCounter = 0
        # End the array
        file.write("};\n\n")

        # Now need to add the Huffman Table
        file.write("// Data for Huffman table \n\n")
        # --- Array 1 of 3 --- The frequency of each length of binary number something or other this needs rewording
        # Get data type for array 1 (almost always uint16_t)
        bitSizeForArray1 = ceil(int.bit_length(max(binCodeLenFreq)) / 8) * 8
        dataTypeArray1 = "uint" + str(bitSizeForArray1) + "_t"
        # Add max binary code size, for c to know the array length
        file.write("uint8_t maxBinCodeSize = " + str(len(binCodeLenFreq)) + ";\n")
        # Add frequency of each binary code size
        file.write(dataTypeArray1 + " binCodeSizes[] = {")
        newLineCounter = 0                  # For placing new lines
        writeCounter = len(binCodeLenFreq)  # For placing commas
        for codeSize in binCodeLenFreq:
            file.write(str(codeSize))
            newLineCounter += 1
            writeCounter -= 1
            if writeCounter > 0:
                file.write(", ")
            if newLineCounter >= BYTES_PER_LINE:
                file.write("\n\t")
                newLineCounter = 0
        file.write("};\n\n")
        # --- Array 2 of 3 - All of the Huffman codes in a long list
        # Smallest first, group into 16 bits
        # For speed, maybe group into multiple arrays based on size?
        # Not great when most of the codes are the same size haha
        # THIS NEEDS TO BE SPLIT INTO BATCHES THAT FIT INTO RAM
        array2Length = 0
        for row in huffmanTable:
            array2Length += len(row[0])
        array2Length = ceil(array2Length / 16)
        file.write("uint16_t array2Size = " + str(array2Length) + ";\n")
        file.write("uint16_t array2Idk[] = {")
        newLineCounter = 0
        # writeCounter = 0
        writeBuffer = ""
        for row in huffmanTable:
            writeBuffer = writeBuffer + row[0]
            if len(writeBuffer) > 16:
                newByte = hex(int(writeBuffer[0:15], 2))
                writeBuffer =  writeBuffer[15:]
                # Force the hex to be 4 digits long
                while len(newByte) < 6:
                    newByte = "0x0" + newByte[2:]
                file.write(newByte + ", ")
                newLineCounter += 1
                # writeCounter += 1
                if newLineCounter >= BYTES_PER_LINE:
                    file.write("\n\t")
                    newLineCounter = 0
        # Code always leaves data to write without a comma
        while len(writeBuffer) < 16:
            writeBuffer = writeBuffer + "0"
        file.write(hex(int(writeBuffer, 2)))
        file.write("};\n\n")
        # --- Array 3 of 3 - The values corresponding to each Huffman code
        file.write("uint16_t array3Thing[] = {")
        newLineCounter = 0
        commaCounter = len(huffmanTable)
        for row in huffmanTable:
            file.write(row[1])
            newLineCounter += 1
            commaCounter -= 1
            if commaCounter > 0:
                file.write(", ")
            if newLineCounter == BYTES_PER_LINE:
                file.write("\n\t")
                newLineCounter = 0
        file.write("};\n\n")
            



