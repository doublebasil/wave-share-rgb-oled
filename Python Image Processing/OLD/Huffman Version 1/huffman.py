from math import pow

"""
This code can be used to create a huffman table for datasets, it is currently
setup to encode a char array

Note that for smaller datasets there are multiple possible huffman trees
"""

def createTable(data):
    # Creating two 1D arrays for item and item-frequency
    dataValue = []
    dataFreq = []
    # Fill the item-frequency arrays using input variable 'data'
    for item in data:
        # If we haven't seen that value before, create a new place for it in the list
        if not item in dataValue:
            dataValue.append(item)
            dataFreq.append(1)
            # If we have already seen that value increase it's frequency by 1
        else:
            # Find where that item is within 'dataValue'
            for i in range(0, len(dataValue)):
                if dataValue[i] == item:
                    dataFreq[i] += 1
                    break

    # dataFreq and dataValue are now filled, combine them into one list 'valueFrequency'
    valueFrequency = []
    for index in range(0, len(dataFreq)):
        valueFrequency.append([dataFreq[index], dataValue[index]])

    # Now build the Huffman tree using big brain loop
    # While valueFrequency has a height > 1, there is still more combining to do
    while len(valueFrequency) > 1:
        # Sort the list by the first column (the frequency column)
        valueFrequency.sort(key=lambda x: x[0])
        # Combine the top two lowest frequencies into a new item
        newItem = [valueFrequency[0][0] + valueFrequency[1][0], [valueFrequency[0][1], valueFrequency[1][1]]]
        # Delete the top two lowest frequencies
        valueFrequency.pop(0)
        valueFrequency.pop(0)
        # And add the new item to the list
        valueFrequency.append(newItem)
    
    # We now have an array that represents the huffman tree
    huffmanArray = valueFrequency[0][1]
    # You could find the char represented by 10101 using huffmanArray[1][0][1][0][1] for example

    # Turn the huffmanArray into a table that shows what each binary number represents
    huffmanTableBinary = []
    huffmanTableValue = []
    # Variable to remember current number of binary digits (1, 2, 3 etc)
    numberOfDigits = 1
    # Variable to break an otherwise infinite while loop
    finished = False
    while True:
        if finished: break
        # This for loop will e.g. loop from 0 to 7 if numberOfDigits = 2
        # or loop from 0 to 15 if numberOfDigits = 3
        for num in range(0, int(pow(2, numberOfDigits))):
            # Convert num to a binary num within string, e.g. bin(5) == '0b101'
            binaryNum = bin(num)
            # Remove the '0b' from the start
            binaryNum = binaryNum[2:]
            # Add zeros to the front until the number of digits is correct
            while len(binaryNum) < numberOfDigits: binaryNum = "0" + binaryNum
            # Check if this binary number is invalid for the huffman tree
            # For example if 1101 is 'c', then 11010 and 11011 are invalid
            # Another example is if 11 is 'f', then 1100, 1101, 1110 and 1111 are all invalid because
            # 11 appears at the start of them.
            # Variable 'skip' can skip this binary number if it is invalid
            skip = False
            for endIndex in range(0, len(binaryNum)):
                if binaryNum[0:endIndex] in huffmanTableBinary:
                    skip = True
                    break
            if skip: continue

            # If we get to here, the binary number is not out of bounds
            # Find out what the binary number represents within our huffmanArray
            target = huffmanArray
            for digit in binaryNum:
                target = target[int(digit)]

            # Check that the binary number's target is not a list
            if type(target) != type([]):
                # If it is not a list, we have found the end of a branch on the Huffman tree
                huffmanTableBinary.append(binaryNum)
                huffmanTableValue.append(target)
                # If we have found all items on the tree, break the while loop
                if len(huffmanTableValue) == len(dataValue):
                    # We have built the tree
                    finished = True
                    break

        numberOfDigits += 1

    # Combine huffmanTableBinary and huffmanTableValue into one list
    huffmanTable = []
    for index in range(0, len(huffmanTableBinary)):
        huffmanTable.append([huffmanTableBinary[index], huffmanTableValue[index]])
    
    # Return the Huffman table
    return huffmanTable


def encode(huffmanTable, imageData):
    encodedImage = []
    buffer = ""
    for pixel in imageData:
        # Find that pixel in huffmanTable
        for row in huffmanTable:
            if row[1] == pixel:
                buffer = row[0] + buffer
                break
        # Check if the buffer has more than 2 bytes of data
        bufferLength = len(buffer)
        if bufferLength >= 16:
            # Remove the last 16 bits from the buffer
            last16Bits = buffer[bufferLength - 16 : bufferLength]
            buffer = buffer[0 : bufferLength - 16]
            # Now turn the 16 bit binary into 4 digit hex
            hexValue = hex(int(last16Bits, 2))
            # Ensure hexValue is four digit, e.g. '0x1234'
            while len(hexValue) < 6: 
                hexValue = "0x0" + hexValue[2:]
            # Add the hex value to the encoded image data
            encodedImage.append(hexValue)
    # We are now left with less than 16 bits, turn this into 4 digit hex
    hexValue = hex(int(buffer, 2))
    while len(hexValue) < 6: 
        hexValue = "0x0" + hexValue[2:]
    encodedImage.append(hexValue)
    # Now return the encoded image
    print(encodedImage)
    return encodedImage


"""
NOTE
There is an issue with this code where I'm actually checking the buffer
in backwards order, whereas the huffman table is (obviously) not backwards.
Need to create a new version where I can make the buffer both not be backwards,
and is processed in a way that this still works.
"""

def _decode(huffmanTable, encodedImage, dataLength):
    decodedData = []        # Function output
    buffer = ""             # Buffer gets filled with binary digits as a string
    itemsFound = 0          # Variable to remember how many characters/items have been found
    currentCheckSize = 1    # Currently checking for binary strings within the table with this length
    # Process all the bytes within the encoded image
    for byte in encodedImage:
        # Convert the byte into binary, and remove the '0b' from the start
        binary = bin(int(byte, 16))[2:]
        # Ensure the binary number is 16 'bits' long
        while len(binary) < 16: binary = "0" + binary
        # Add the binary number to the buffer
        buffer = binary + buffer
        print("Adding a new byte")
        # Keep finding strings of binary from the huffman table
        while True:
            foundString = False
            while currentCheckSize <= len(buffer):
                # Check if our currentCheckSize matches anything in the huffman table
                for row in huffmanTable:
                    # Check that the binary string in this row is the correct length
                    if len(row[0]) == currentCheckSize:

                        print("Checking " + str(buffer) + " against " + str(row) + ", currentCheckSize = " + str(currentCheckSize))

                        # Check that we have found a binary pattern in within the buffer
                        bufferLength = len(buffer)
                        if buffer[bufferLength-currentCheckSize : bufferLength] == row[0]:

                            print("That's a match!")

                            # Code has matched a binary string
                            buffer = buffer[0 : bufferLength - currentCheckSize]
                            decodedData.append(row[1])
                            foundString = True
                            currentCheckSize = 1
                            itemsFound += 1
                            break
                    # If the binary string is too big, break the for loop
                    elif len(row[0]) > currentCheckSize: break
                currentCheckSize += 1
            # If we didn't find anything, add the next byte of data to the buffer                
            if foundString == False:
                break
        # If we have found all the data points, end this function by breaking
        if itemsFound == dataLength: break
    return decodedData


