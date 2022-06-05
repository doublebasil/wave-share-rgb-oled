import os
from math import ceil

# Some setting constants here
ELEMENTS_PER_LINE = 4   # This changes how the file is written, no effect on performance
ELEMENTS_PER_BATCH = 50    # This one will affect perfomance, but I haven't tested yet.

def _writeEncodedData(file, encodedData):
    # Add comment to header file
    file.write("// Encoded data for the image \n\n")
    # Data is split into many arrays reffered to as batches. Find number of batches required
    numberOfBatches = ceil(len(encodedData) / ELEMENTS_PER_BATCH)
    # The last batch will have less elements, find how many elements it will have
    bytesInFinalBatch = len(encodedData) % ELEMENTS_PER_BATCH
    # Write each batch
    for batchNumber in range(0, numberOfBatches):
        # Create a 16 bit unsigned integer array
        file.write("uint16_t dataBatch" + str(batchNumber) + "[] = {\n\t")
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
    file.write("uint16_t* dataPointers[] = {\n\t")
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
    file.write("uint16_t maxBinCodeLen = " + str(len(binCodeLenFreq)) + ";\n")
    # Add frequency of each binary code size
    file.write("uint16_t binCodeSizes[] = {")
    newLineCounter = 0                  # For placing new lines
    writesRemaining = len(binCodeLenFreq)  # For placing commas
    for codeSize in binCodeLenFreq:
        file.write(str(codeSize))
        newLineCounter += 1
        writesRemaining -= 1    # Note that this variable decreases
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
    array2Length = 0
    for row in huffmanTable:
        array2Length += len(row[0])
    array2Length = ceil(array2Length / 16)
    file.write("uint16_t huffInputLength = " + str(array2Length) + ";\n")
    file.write("uint16_t huffInput[] = {")
    newLineCounter = 0
    writeBuffer = ""
    for row in huffmanTable:
        writeBuffer = writeBuffer + row[0]
        if len(writeBuffer) > 16:
            # Move the first 16 bits from the buffer and write to the header file
            newElement = hex(int(writeBuffer[0:16], 2))
            writeBuffer =  writeBuffer[16:]
            # Ensure newElement has 4 digits, e.g. 0x1234
            while len(newElement) < 6:
                newElement = "0x0" + newElement[2:]
            file.write(newElement + ", ")
            newLineCounter += 1
            # Add new line if there are enough elements on the current line
            if newLineCounter >= ELEMENTS_PER_LINE:
                file.write("\n\t")
                newLineCounter = 0
    # Code always leaves one element to write, with no following comma
    # Append 0 to the end of the buffer until the buffer has 16 bits
    while len(writeBuffer) < 16:
        writeBuffer = writeBuffer + "0"
    file.write(hex(int(writeBuffer, 2)))
    file.write("};\n\n")

    # --- Array 3 of 3 - huffOutput
    # The values corresponding to each Huffman code
    file.write("uint16_t huffOutput[] = {\n\t")
    newLineCounter = 0
    commaCounter = len(huffmanTable)
    for row in huffmanTable:
        file.write(row[1])
        newLineCounter += 1
        commaCounter -= 1
        if commaCounter > 0:
            file.write(", ")
        if newLineCounter == ELEMENTS_PER_LINE:
            file.write("\n\t")
            newLineCounter = 0
    file.write("};\n\n")


def generateHeaderFile(huffmanTable, encodedData):
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
        # Write the encoded data to the header file
        _writeEncodedData(file, encodedData)
        # Write the decoding data to the header file
        _writeHuffmanTable(file, huffmanTable)

        

            



