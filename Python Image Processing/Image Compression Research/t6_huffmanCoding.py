from math import pow

"""
This code can be used to create a huffman table for datasets, it is currently
setup to encode a char array

Note that for smaller datasets there are multiple possible huffman trees
"""

def huffmanTree(data):
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

def main():
    myString = "this is a string, and it shall be used to show how this huffman coding script works"
    myCharArray = []
    for ch in myString:
        myCharArray.append(ch)
    h = huffmanTree(myCharArray)
    print(h)

if __name__ == '__main__':
    main()
    

    
