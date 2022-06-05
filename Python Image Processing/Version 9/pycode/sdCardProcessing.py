from math import floor

def _bytesToCharBlock(byte1, byte2, byte3):
    # Combine the three bytes into a 24 digits hex number
    cat = byte1[2:] + byte2[2:] + byte3[2:]
    # Convert into binary
    cat = bin(int(cat, 16))
    # Remove the "0b" from the start of the binary number
    cat = cat[2:]
    # Ensure cat is 48 bits long (6 * 8 = 48, 6 bytes with 8 bits = 48 bits total)
    cat = ("0" * (48 - len(cat))) + cat
    # Create output variable
    output = ""
    # Split cat into eight 6-digit binary numbers
    for index in range(0, 48, 6):
        output = output + chr(int("0b" + cat[index:index+6], 2) + 32)

    print(cat)
    print(output)
    a = input("pause")
    return cat

def createSDFile(huffmanTable, encodedData, displayWidth, displayHeight):

    for i in range(0, 3 * floor(len(encodedData) / 3), 3):
        charBlock = _bytesToCharBlock(encodedData[i], encodedData[i + 1], encodedData[i + 2])

