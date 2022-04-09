from turtle import left
from PIL import Image
from math import pow
import numpy as np

from time import sleep as sl

"""
Attempting to use huffman coding to compress images

Thoughts:
    in c I could implement the huffman table with pointers and 1x2 arrays
    in python I could implement the table with 1x2 lists within list

    Making the table is gonna be a brainf

"""

def rgbTo16Bit(rgb):
    return (rgb[0] << 11) + (rgb[1] << 5) + rgb[2]

def huffmanTree(data):
    # Creating two 1D arrays for item frequency
    dataValue = []
    dataFreq = []
    # Fill the item
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

    # valueFrequency = np.array([dataFreq, dataValue])
    # print(valueFrequency)
    # valueFrequency.sort(axis=1)
    # print(valueFrequency)

    # valueFrequency = [dataFreq, dataValue]
    # print(valueFrequency)
    # valueFrequency.sort(key=lambda x: x[0])
    # print(valueFrequency)

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
    return valueFrequency[0][1]

def drawHuffmanTree(h):
    # # Find distance from left
    # leftToCenter = 0
    # v = h
    # while type(v) == type([]):
    #     v = v[0]
    #     leftToCenter += 1
    # print(leftToCenter)
    
    itemsPrinted = 0
    iteration = 0
    treeString = ""
    prevBinaryNumLength = 1
    while True:
        print("--- Iteration " + str(iteration) + " --- ")
        treePath = bin(iteration) # Returns string
        treePath = treePath[2:]
        print("Iteration " + str(iteration) + " -> " + treePath)
        newBinaryNumLength = len(treePath)
        print("New digits: " + str(newBinaryNumLength) + ", Old digits: " + str(prevBinaryNumLength))
        if newBinaryNumLength > prevBinaryNumLength:
            print("Adding a new line")
            treeString += "\n"
        prevBinaryNumLength = newBinaryNumLength
        t = h
        for n in treePath:
            t = t[int(n)]
        if type(t[0]) != type([]):
            treeString += str(t)
            itemsPrinted += 1
        else:
            treeString += "#"
        iteration += 1
        print(treeString)
        sl(1)


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
    drawHuffmanTree(h)

    
