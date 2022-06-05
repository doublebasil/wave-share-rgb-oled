from curses.ascii import HT
import tempfile
import huffman
import imageProcessing

def main():
    # imageData = imageProcessing.getImageData()
    
    # print("Raw image uses " + str(len(imageData) * 2) + " bytes")

    # hTable = huffman.createTable(imageData)

    encodeTestString = "this is a to test the thing"
    encodeTestCharArray = []
    for ch in encodeTestString:
        encodeTestCharArray.append(ch)
    hTable = huffman.createTable(encodeTestCharArray)
    print(hTable)
    encodedImage = huffman.encode(hTable, encodeTestCharArray)
    decodedImage = huffman._decode(hTable, encodedImage, len(encodeTestString))
    print(decodedImage)

    # st = "this is a test"
    # cha = []
    # for ch in st:
    #     cha.append(ch)
    # h = huffman.createTable(cha)
    # print(h)

if __name__ == '__main__':
    main()