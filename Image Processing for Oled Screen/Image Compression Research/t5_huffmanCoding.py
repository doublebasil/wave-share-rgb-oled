from PIL import Image
from math import pow

from time import sleep as sl

"""
Attempting to use huffman coding to compress images

Thoughts:
    in c I could implement the huffman table with pointers and 1x2 arrays
    in python I could implement the table with 1x2 lists within list

    Making the table is gonna be a brainf

    Note! For smaller datasets there are multiple possible huffman trees
"""

def rgbTo16Bit(rgb):
    return (rgb[0] << 11) + (rgb[1] << 5) + rgb[2]

def huffmanTree(data):
    # Creating two 1D arrays for item frequency
    dataValue = []
    dataFreq = []
    # Fill the item-frequency arrays
    for item in data:
        if not item in dataValue:
            dataValue.append(item)
            dataFreq.append(1)
        else:
            # Find where that item is within 'value'
            for i in range(0, len(dataValue)):
                if dataValue[i] == item:
                    dataFreq[i] += 1
                    break

    # dataFreq and dataValue are now filled, combine them
    valueFrequency = []
    for index in range(0, len(dataFreq)):
        valueFrequency.append([dataFreq[index], dataValue[index]])

    # Now build the hoffman tree using big brain loop
    while len(valueFrequency) > 1:
        valueFrequency.sort(key=lambda x: x[0])
        newItem = [valueFrequency[0][0] + valueFrequency[1][0], [valueFrequency[0][1], valueFrequency[1][1]]]
        valueFrequency.pop(0)
        valueFrequency.pop(0)
        valueFrequency.append(newItem)
    # We now have an array that represents the huffman tree
    huffmanArray = valueFrequency[0][1]

    # Draw the huffman tree
    huffmanTableBinary = []
    huffmanTableValue = []
    numberOfDigits = 1 # Number of binary digits
    finished = False
    while True:
        if finished: break
        for num in range(0, int(pow(2, numberOfDigits))):
            # Convert num to a binary num within string, e.g. bin(5) == '0b101'
            binaryNum = bin(num)
            # Remove the '0b' from the start
            binaryNum = binaryNum[2:]
            # Add zeros to the front until the number of digits is correct
            while len(binaryNum) < numberOfDigits: binaryNum = "0" + binaryNum

            # Check if this binary number is invalid for the huffman tree
            skip = False
            for endIndex in range(0, len(binaryNum)):
                if binaryNum[0:endIndex] in huffmanTableBinary:
                    skip = True
                    break
            if skip: continue

            # We aren't out of bounds, find what the binary number represents
            target = huffmanArray
            for digit in binaryNum:
                target = target[int(digit)]

            # Check for non-list
            if type(target) != type([]):
                huffmanTableBinary.append(binaryNum)
                huffmanTableValue.append(target)
                if len(huffmanTableValue) == len(dataValue):
                    # We have built the tree
                    finished = True
                    break
            if finished: break

        numberOfDigits += 1

    # Combine huffmanTableBinary and huffmanTableValue
    huffmanTable = []
    for index in range(0, len(huffmanTableBinary)):
        huffmanTable.append([huffmanTableBinary[index], huffmanTableValue[index]])
    
    # Return the Huffman table and then the Huffman Array
    return huffmanTable


# def drawHuffmanTree(h):
#     # # Find distance from left
#     # leftToCenter = 0
#     # v = h
#     # while type(v) == type([]):
#     #     v = v[0]
#     #     leftToCenter += 1
#     # print(leftToCenter)
    
#     huffmanTableBinary = []
#     huffmanTableItems = []

#     itemsPrinted = 0
#     iteration = 0
#     treeString = ""
#     prevBinaryNumLength = 1
#     while True:
#         print("--- Iteration " + str(iteration) + " --- ")
#         binaryNum = bin(iteration) # Returns string
#         binaryNum = binaryNum[2:]
#         print("Iteration " + str(iteration) + " -> " + binaryNum)
#         newBinaryNumLength = len(binaryNum)
#         print("New digits: " + str(newBinaryNumLength) + ", Old digits: " + str(prevBinaryNumLength))
#         if newBinaryNumLength > prevBinaryNumLength:
#             print("Adding a new line")
#             treeString += "\n"
#         prevBinaryNumLength = newBinaryNumLength
#         t = h
#         binaryTest = ""
#         skip = False
#         for n in binaryNum:
#             binaryTest += n
#             if binaryTest in huffmanTableBinary:
#                 skip = True
#                 break
#             t = t[int(n)]
#         iteration += 1
#         if skip == True:
#             continue
        
#         # if type(t[0]) != type([]):
#         #     treeString += str(t)
#         #     itemsPrinted += 1
#         # else:
#         #     treeString += "#"
#         # iteration += 1
#         # print(treeString)
#         # sl(1)

#         # Check if taking the next left or right gives a non-list
#         for f in range(0, 2):
#             if type(t[f]) != type([]):
#                 huffmanTableBinary.append(binaryNum + str(f))
#                 huffmanTableBinary.append(t[f])
#                 treeString += t[f]

#             else:
#                 treeString += "#"

#         print(treeString)
#         sl(1.5)


def main():
    im = Image.open('128x128.png')
    rgbData = list(im.getdata())

if __name__ == '__main__':
    # main()

    # print(rgbTo16Bit((31, 63, 31)))
    # print(pow(2, 16) - 1)

    # This does sort by only the first column, which is good
    # a = [[2, 'b'], [3, 'c'], [1, 'a'], [0, 'j']]
    # a.sort()
    # print(a)

    # testData = [1, 2, 3, 2, 3, 4, 3, 2, 4, 1]
    testData = ['a', 'b', 'a', 'c', 'u', 's', 'i', 's', 'a', 'g', 'o', 'o', 'd', 'w', 'o', 'r', 'd']
    h = huffmanTree(testData)

    print(h)

    
