import huffman
import imageProcessing
import arduinoProcessing
import txtGenerator

def main():
    # imageData = imageProcessing.getImageData()
    
    # print("Raw image uses " + str(len(imageData) * 2) + " bytes")

    # hTable = huffman.createTable(imageData)

    # encodeTestString = "this is a to test the thing"
    # encodeTestString = "why would you want to become a programmer?"
    # encodeTestCharArray = []
    # for ch in encodeTestString:
    #     encodeTestCharArray.append(ch)
    # hTable = huffman.createTable(encodeTestCharArray)
    # encodedImage = huffman.encode(hTable, encodeTestCharArray)

    # print(hTable)

    # binaryString = ""
    # for byte in encodedImage:
    #     binaryTemp = bin(int(byte, 16))[2:]
    #     while len(binaryTemp) < 16: binaryTemp = "0" + binaryTemp
    #     binaryString += binaryTemp
    # print(binaryString)

    # decodedImage = huffman._decode(hTable, encodedImage, len(encodeTestString))
    # print(decodedImage)



    # Ask for oled Width and Height
    displayWidth = int(input("What is your oled display's width? "))
    if displayWidth <= 0:
        exit("Error - invalid display width")
    displayHeight = int(input("What is your oled display's height? "))
    if displayHeight <= 0:
        exit("\nError - invalid display width")
    imageData = imageProcessing.getImageData(displayWidth, displayHeight)
    print(imageData)
    exit()
    print("Raw image uses " + str(len(imageData) * 2) + " bytes")
    hTable = huffman.createTable(imageData)
    print("Encoding image...")
    encodedImage = huffman.encode(hTable, imageData)
    print("Encoded image uses " + str(len(encodedImage) * 2) + " bytes")
    arduinoProcessing.generateHeaderFile(hTable, encodedImage, displayWidth, displayHeight)
    print("Generating txt version of Huffman table")
    txtGenerator.generateHuffmanTableTxt(hTable)
    print("Done!")

if __name__ == '__main__':
    main()