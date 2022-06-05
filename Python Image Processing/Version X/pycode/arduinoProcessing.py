# THIS FILE HAS BEEN DISCONTINUED :(

import os
from math import ceil

# Some setting constants here
ELEMENTS_PER_LINE = 4   # This changes how the file is written, no effect on performance
ELEMENTS_PER_BATCH = 50 # This one will affect perfomance, but I haven't tested yet.

# This variable can be set to "" if the header variables do not need to be extern
# externPrefix = "extern "
externPrefix = ""

def _writeEncodedData(file, encodedData):
    # Add comment to header file
    file.write("// Encoded data for the image \n\n")
    # Data is split into many arrays referred to as batches. Find number of batches required
    numberOfBatches = ceil(len(encodedData) / ELEMENTS_PER_BATCH)
    # The last batch will have less elements, find how many elements it will have
    bytesInFinalBatch = len(encodedData) % ELEMENTS_PER_BATCH
    # Write each batch
    for batchNumber in range(0, numberOfBatches):
        # Create a 16 bit unsigned integer array
        file.write(externPrefix + "uint16_t dataBatch" + str(batchNumber) + "[] = {\n\t")
        newLineCounter = 0  # Add a counter for noting when to add new lines
        writeCounter = 0    # Add a write counter to know all bytes are written
        for b in encodedData[batchNumber * ELEMENTS_PER_BATCH : (batchNumber + 1) * ELEMENTS_PER_BATCH]:
            # Write that byte to the header file
            file.write(b)
            # Increment the counters
            writeCounter += 1
            newLineCounter += 1
            # If this is the last batch to be written
            if batchNumber == numberOfBatches - 1:
                # If this is not the last element of the batch, add a comma
                if writeCounter != bytesInFinalBatch:
                    file.write(", ")
            # If this is not the last batch
            else:
                # If this is not the last element of the batch, add a comma
                if writeCounter != ELEMENTS_PER_BATCH:
                    file.write(", ")
            # Add a new line if there are enough elements on the current line
            if newLineCounter >= ELEMENTS_PER_LINE:
                file.write("\n\t")
                newLineCounter = 0
        # End this batch array
        file.write("};\n")
    # Create an array of pointers that point to the start of each batch
    file.write("// Array of pointers to encoded data \n\n")
    file.write(externPrefix + "uint16_t* dataPointers[] = {\n\t")
    # Counter for noting when to add new lines
    newLineCounter = 0
    # For each batch, add a pointer to that batch
    for batchNumber in range(0, numberOfBatches):
        file.write("&dataBatch" + str(batchNumber) + "[0]")
        newLineCounter += 1
        # Add a comma if this isn't the last pointer
        if batchNumber != (numberOfBatches - 1):
            file.write(", ")
        # Add a new line if there are enough elements on the current line
        if newLineCounter >= ELEMENTS_PER_LINE: 
            file.write("\n\t")
            newLineCounter = 0
    # End the array
    file.write("};\n\n")
    # Note how many arrays were used
    file.write(externPrefix + "uint16_t ENCODING_ARRAYS_USED = " + str(numberOfBatches) + ";\n")

def _writeHuffmanTable(file, huffmanTable):
    # Some code for storing the Huffman table
    # My (potentially horrendus) method will create 3 arrays to store the table
    # 1 - binCodeLenFreq
    #     Number of each length of binary number in Huffman Code
    # 2 - huffInput
    #     All the huffman codes in a long binary list, seperated into
    #     an array of uint16_t (probably)
    # 3 - huffOutput
    #     The values that each binary code represent, in order 
    #     corresponding to array 2

    # Collect data for array 1 - binCodeLenFreq
    # e.g. third element will tell you how many codes have 3 binary digits
    # This loop utilises the codes being in size order within the huffmanTable variable
    binCodeLenFreq = []
    currentLength = 0
    for row in huffmanTable:
        binaryCode = row[0]
        binaryCodeLen = len(binaryCode)
        while currentLength < binaryCodeLen:
            binCodeLenFreq.append(0)
            currentLength += 1
        binCodeLenFreq[currentLength-1] += 1

    # Add comment before code for Huffman Table data
    file.write("// Arrays for Huffman table \n\n")

    # --- Array 1 of 3 --- binCodeLenFreq

    # Add variable for length of array (this may need adjusting?)
    file.write(externPrefix + "uint8_t maxBinCodeLen = " + str(len(binCodeLenFreq)) + ";\n")
    # Add frequency of each binary code size
    file.write("// Maybe in future change this to cumulative frequency\n")
    file.write(externPrefix + "uint16_t binCodeSizes[] = {")
    newLineCounter = 0                      # For placing new lines
    writesRemaining = len(binCodeLenFreq)   # For placing commas
    for codeSize in binCodeLenFreq:
        file.write(str(codeSize))
        newLineCounter += 1
        writesRemaining -= 1    # Note that this variable decreases to 0
        if writesRemaining > 0:
            file.write(", ")
        if newLineCounter >= (ELEMENTS_PER_LINE * 3):
            file.write("\n\t")
            newLineCounter = 0
    file.write("};\n\n")

    # --- Array 2 of 3 - huffInput 
    # All of the Huffman codes in a long list, shortest first,
    # Group into 16 bits for storing in an array
    # THIS NEEDS TO BE SPLIT INTO BATCHES THAT FIT INTO RAM
    
    # Find the total number of 16 bit integers required for this array
    huffInputRequiredElements = 0
    for row in huffmanTable:
        huffInputRequiredElements += len(row[0])
    huffInputRequiredElements = ceil(huffInputRequiredElements / 16)
    # The next line may be unnecessary
    file.write("// uint16_t huffInputLength = " + str(huffInputRequiredElements) + ";\n")
    # Initialise counters and buffer
    newLineCounter = 0          # For adding new lines
    newArrayCounter = ELEMENTS_PER_BATCH # For starting a new array when one gets too big. Inital value forces first array to be created
    arraysUsed = 0              # Self-explanatory, for creating the pointer array afterwards
    totalElementsWritten = 0    # Elements written across all arrays
    writeBuffer = ""            # Buffer is filled with binary until it contains >= 2 bytes
    # Process each row of the Huffman table
    for row in huffmanTable:
        # Create new array if necessary (this will always happen on the first iteration)
        if newArrayCounter == ELEMENTS_PER_BATCH:
            # If this isn't the first array, end the previous array
            if arraysUsed != 0:
                file.write("};\n")
            # Start the next array
            file.write(externPrefix + "uint16_t huffInputData" + str(arraysUsed) + "[] = {\n\t")
            newArrayCounter = 0 # Reset
            newLineCounter = 0  # Reset
            arraysUsed += 1     # Increment
        # Add the huffman code to the end of the buffer
        writeBuffer = writeBuffer + row[0]
        # Write 16 bits from the buffer to the header file if buffer has enough bits
        if len(writeBuffer) > 16:
            newElement = hex(int(writeBuffer[0:16], 2))
            writeBuffer = writeBuffer[16:]
            # Ensure new element has 4 hex digits e.g. 0xabcd
            while len(newElement) < 6: newElement = "0x0" + newElement[2:]
            # Write new element to file
            file.write(newElement)
            # Increment counters
            newLineCounter += 1
            newArrayCounter += 1
            totalElementsWritten += 1
            # Check if comma is required
            if (not (totalElementsWritten == (huffInputRequiredElements-1))) and (not (newArrayCounter == ELEMENTS_PER_BATCH)):
                file.write(", ")
            # Check if new line is required
            if newLineCounter == ELEMENTS_PER_LINE:
                file.write("\n\t")
                newLineCounter = 0
    # If there is still data in the buffer, add a final byte
    if len(writeBuffer) > 0:
        # Make the writeBuffer 16 characters long
        for i in range(0, 16 - len(writeBuffer)):
            writeBuffer += "0"
        # And write the writeBuffer to the file
        newElement = hex(int(writeBuffer, 2))
        while len(newElement) < 6: newElement = "0x0" + newElement[2:]
        file.write(", " + newElement)
    # End last array
    file.write("};\n\n")
    # Create array of pointers
    file.write("// Pointers for array 2\n\n")
    file.write(externPrefix + "uint16_t *huffInput[] = {\n\t")
    newLineCounter = 0
    for n in range(0, arraysUsed):
        file.write("&huffInputData" + str(n) + "[0]")
        newLineCounter += 1
        if n != (arraysUsed - 1):
            file.write(", ")
        if newLineCounter == ELEMENTS_PER_LINE:
            file.write("\n\t")
            newLineCounter = 0
    file.write("};\n\n")

    # --- Array 3 of 3 - huffOutput
    # The values corresponding to each Huffman code
    file.write("// Data for array 3\n\n")
    # Find total number of elements needed
    huffOutputRequiredElements = len(huffmanTable)
    # Counters
    newLineCounter = 0          # For adding new lines
    newArrayCounter = ELEMENTS_PER_BATCH # For starting a new array. Initial value forces first iteration to create the first array
    arraysUsed = 0              # For creating the array of pointers
    totalElementsWritten = 0    # Accross all arrays. Used for comma placement
    # Add data from the Huffman table
    for row in huffmanTable:
        # Create a new array if necessary (this will always happen on the first iteration)
        if newArrayCounter == ELEMENTS_PER_BATCH:
            # If this isn't the first array, end the previous        
            if arraysUsed != 0:
                file.write("};\n")
            # Start the next array
            file.write(externPrefix + "uint16_t huffOutputData" + str(arraysUsed) + "[] = {\n\t")
            newArrayCounter = 0 # Reset
            newLineCounter = 0  # Reset
            arraysUsed += 1     # Increment
        # Write the output code to the file
        file.write(row[1])
        # Increment counters
        newLineCounter += 1
        newArrayCounter += 1
        totalElementsWritten += 1
        # Add a comma if necessary
        if (not (totalElementsWritten == (huffOutputRequiredElements)) and (not (newArrayCounter == ELEMENTS_PER_BATCH))):
            file.write(", ")
        # Check if new line is required
        if newLineCounter == ELEMENTS_PER_LINE:
            file.write("\n\t")
            newLineCounter = 0
    # End last array
    file.write("};\n\n")
    # Create array of pointers
    file.write("// Pointers for array 3\n\n")
    file.write(externPrefix + "uint16_t *huffOutput[] = {\n\t")
    newLineCounter = 0
    for n in range(0, arraysUsed):
        file.write("&huffOutputData" + str(n) + "[0]")
        newLineCounter += 1
        if n != (arraysUsed - 1):
            file.write(", ")
        if newLineCounter == ELEMENTS_PER_LINE:
            file.write("\n\t")
            newLineCounter = 0
    file.write("};\n\n")


def generateHeaderFile(huffmanTable, encodedData, displayWidth, displayHeight):
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
    # Create a new header file called image.h
    with open('image.h', 'w') as file:
        # Add stdint.h to the header file
        file.write("#include <stdint.h>\n\n")
        # Note the standard array size
        file.write(externPrefix + "uint16_t ARRAY_SIZE = " + str(ELEMENTS_PER_BATCH) + ";\n\n")
        # And note the display width and height
        file.write(externPrefix + "uint16_t DISPLAY_WIDTH = " + str(displayWidth) + ";\n")
        file.write(externPrefix + "uint16_t DISPLAY_HEIGHT = " + str(displayHeight) + ";\n\n")
        # Write the encoded data to the header file
        _writeEncodedData(file, encodedData)
        # Write the decoding data to the header file
        _writeHuffmanTable(file, huffmanTable)

        

            



