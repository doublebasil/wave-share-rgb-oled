from math import floor

import os

# A word is two bytes
def _wordsToCharBlock(word1, word2, word3):
    # Combine the three words into a 24 digits hex number
    cat = word1[2:] + word2[2:] + word3[2:]
    # Convert into binary
    cat = bin(int(cat, 16))
    # Remove the "0b" from the start of the binary number
    cat = cat[2:]
    # Ensure cat is 48 bits long (6 * 8 = 48, 6 words with 8 bits = 48 bits total)
    cat = ("0" * (48 - len(cat))) + cat
    # Create output variable
    output = ""
    # Split cat into eight 6-digit binary numbers
    for index in range(0, 48, 6):
        output = output + chr(int("0b" + cat[index:index+6], 2) + 32)
    return output

def _numToCharBlock(num, numberOfCharacters):
    # Convert num into binary
    num = (bin(num))[2:]
    # Check that the number of characters used is sufficient
    if len(num) > (numberOfCharacters * 6):
        exit(str(num) + " cannot be converted to characters for sd card")
    # Ensure num is the correct length
    num = ("0" * ((numberOfCharacters * 6) - len(num))) + num
    
    output = ""
    for i in range(0, numberOfCharacters * 6, 6):
        output = output + chr(int("0b" + num[i:i+6], 2) + 32)

    print(output)

    i = input("PAUSE")
    return output

def createSDFile(huffmanTable, encodedData, displayWidth, displayHeight):

    # os.system("gio trash \"encoded data\"")
    # with open('encoded data', 'w') as file:
    #     for thing in encodedData:
    #         file.write(thing)
    #         file.write("\n")

    # --- Convert the encodedData into data for the SD card
    sdData_encoded = ""
    for i in range(0, 3 * floor(len(encodedData) / 3), 3):
        sdData_encoded = sdData_encoded + _wordsToCharBlock(encodedData[i], encodedData[i + 1], encodedData[i + 2])
        # print(encodedData[i])
        # print(encodedData[i+1])
        # print(encodedData[i+2])
    # We've done as many blocks of 3 as possible, there may still 1 or 2 words left
    if (floor(len(encodedData) / 3) * 3) != len(encodedData):
        remainingWords = []
        for i in range(floor(len(encodedData) / 3) * 3, len(encodedData)):
            # print(encodedData[i])
            remainingWords.append((encodedData[i])[2:])
        # Fill this with empty Words
        while len(remainingWords) < 3:
            remainingWords.append("0" * 4)
        # print(remainingWords)
        sdData_encoded = sdData_encoded + _wordsToCharBlock(remainingWords[0], remainingWords[1], remainingWords[2])
    
    # --- Convert the table inputs and outputs into SD card readable data
    tableInputBuffer = ""
    sdData_tableInput = ""
    tableOutputBuffer = []
    sdData_tableOutput = ""
    tableInputSizeFrequency = []
    for row in huffmanTable:
        while len(row[0]) > len(tableInputSizeFrequency):
            tableInputSizeFrequency.append(0)
        tableInputSizeFrequency[len(row[0]) - 1] = tableInputSizeFrequency[len(row[0]) - 1] + 1

        tableInputBuffer = tableInputBuffer + row[0]
        tableOutputBuffer.append(row[1])
        
        if len(tableInputBuffer) >= 48:
            print(tableInputBuffer)
            word1 = hex(int("0b" + tableInputBuffer[0:16], 2))
            word2 = hex(int("0b" + tableInputBuffer[16:32], 2))
            word3 = hex(int("0b" + tableInputBuffer[32:48], 2))
            sdData_tableInput = sdData_tableInput + _wordsToCharBlock(word1, word2, word3)
            tableInputBuffer = tableInputBuffer[48:]

        if len(tableOutputBuffer) == 3:
            sdData_tableOutput = sdData_tableOutput + _wordsToCharBlock(tableOutputBuffer[0], tableOutputBuffer[1], tableOutputBuffer[2])

    print(tableInputSizeFrequency)
    sdData_tableInputSizeFrequency = ""
    for freq in tableInputSizeFrequency:
        sdData_tableInputSizeFrequency = sdData_tableInputSizeFrequency + (_numToCharBlock(freq, 3))
    
    sdData_tableInputSizeMaximum = _numToCharBlock(len(tableInputSizeFrequency) - 1, 2)

    # --- Now have almost all the data needed. Can start creating the file
    if os.path.exists('IMAGEDATA.TXT'):
        os.system("gio trash \"IMAGEDATA.TXT\"")
    with open("IMAGEDATA.TXT") as file:
        
    

