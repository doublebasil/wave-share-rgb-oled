from curses.ascii import HT
import tempfile
import huffman
import imageProcessing

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


    imageData = imageProcessing.getImageData()
    print("Raw image uses " + str(len(imageData) * 2) + " bytes")
    hTable = huffman.createTable(imageData)
    print("Encoding image...")
    encodedImage = huffman.encode(hTable, imageData)
    print("Encoded image uses " + str(len(encodedImage) * 2) + " bytes")

if __name__ == '__main__':
    main()