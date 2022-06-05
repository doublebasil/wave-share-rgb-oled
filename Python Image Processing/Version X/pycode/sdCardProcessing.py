from math import floor

import os

# A word is two bytes
def _wordsToCharBlock(word1, word2, word3):
    # Combine the three words into a 24 digit hex number
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

    return output

def createSDFile(imageData, displayWidth, displayHeight):

    # os.system("gio trash \"encoded data\"")
    # with open('encoded data', 'w') as file:
    #     for thing in imageData:
    #         file.write(thing)
    #         file.write("\n")

    # --- Convert the imageData into data for the SD card
    sdData_encoded = ""
    for i in range(0, 3 * floor(len(imageData) / 3), 3):
        sdData_encoded = sdData_encoded + _wordsToCharBlock(imageData[i], imageData[i + 1], imageData[i + 2])
        print(imageData[i] + ", ", imageData[i+1] + ", " + imageData[i+2])
    # We've done as many blocks of 3 as possible, there may still 1 or 2 words left
    if (floor(len(imageData) / 3) * 3) != len(imageData):
        remainingWords = []
        for i in range(floor(len(imageData) / 3) * 3, len(imageData)):
            remainingWords.append((imageData[i])[2:])
        # Fill this with empty Words
        while len(remainingWords) < 3:
            remainingWords.append("0" * 4)

        print(remainingWords)
        print("Adding \"" + _wordsToCharBlock(remainingWords[0], remainingWords[1], remainingWords[2])  + "\"")

        sdData_encoded = sdData_encoded + _wordsToCharBlock(remainingWords[0], remainingWords[1], remainingWords[2])
    
    # Convert image width and height into 3 characters each
    sdData_imageWidth = _numToCharBlock(displayWidth, 3)
    sdData_imageHeight = _numToCharBlock(displayHeight, 3)

    # --- Now create the file
    if os.path.exists('IM.TXT'):
        os.system("gio trash \"IM.TXT\"")
    with open("IM.TXT", 'w') as file:
        file.write(sdData_imageWidth)
        file.write(sdData_imageHeight)
        file.write(sdData_encoded)

        
    

